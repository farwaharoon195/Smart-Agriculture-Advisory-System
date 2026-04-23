import logging
import os
import sqlite3
from datetime import datetime
from functools import wraps

import requests
from flask import Flask, flash, g, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from utils.advisory import (
    detect_disease_by_image_name,
    irrigation_advice,
    recommend_crops,
    simulate_sms_alert,
)
from utils.model_utils import load_or_train_price_model, predict_market_price

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "smart_agri.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, "app.log")),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

price_model = load_or_train_price_model(os.path.join(BASE_DIR, "models", "price_model.pkl"))


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            phone TEXT
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS advisories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            advisory_type TEXT NOT NULL,
            input_data TEXT,
            result TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )
    db.commit()
    logger.info("Database initialized")


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.before_request
def set_language():
    g.lang = session.get("lang", "en")


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/set-language", methods=["POST"])
def set_language_route():
    lang = request.form.get("lang", "en")
    if lang not in ["en", "ur"]:
        lang = "en"
    session["lang"] = lang
    return redirect(request.referrer or url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        phone = request.form.get("phone", "").strip()

        if not username or not password:
            flash("Username and password are required.", "danger")
            return redirect(url_for("register"))

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password_hash, phone) VALUES (?, ?, ?)",
                (username, generate_password_hash(password), phone),
            )
            db.commit()
            flash("Registration successful. Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists.", "danger")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid username or password.", "danger")
            return redirect(url_for("login"))

        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        flash("Welcome back!", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("home"))


def fetch_weather(city="Lahore"):
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if api_key:
        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "appid": api_key, "units": "metric"},
                timeout=5,
            )
            response.raise_for_status()
            payload = response.json()
            return {
                "source": "openweather",
                "temperature": payload["main"]["temp"],
                "humidity": payload["main"]["humidity"],
                "description": payload["weather"][0]["description"],
            }
        except requests.RequestException as exc:
            logger.warning("Weather API call failed, using mock data: %s", exc)

    return {
        "source": "mock",
        "temperature": 31,
        "humidity": 54,
        "description": "Partly cloudy",
    }


@app.route("/dashboard")
@login_required
def dashboard():
    weather = fetch_weather("Lahore")
    return render_template("dashboard.html", weather=weather)


@app.route("/crop", methods=["POST"])
@login_required
def crop_recommendation():
    soil = request.form.get("soil", "")
    season = request.form.get("season", "")
    weather = request.form.get("weather", "")
    crops = recommend_crops(soil, season, weather)

    save_advisory("crop", f"soil={soil},season={season},weather={weather}", ", ".join(crops))
    return jsonify({"recommended_crops": crops})


@app.route("/disease", methods=["POST"])
@login_required
def disease_detection():
    image = request.files.get("image")
    filename = image.filename if image and image.filename else ""

    if image and filename:
        safe_name = filename.replace(" ", "_")
        path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
        image.save(path)
        diagnosis = detect_disease_by_image_name(safe_name)
        input_ref = safe_name
    else:
        symptoms = request.form.get("symptoms", "")
        diagnosis = "Possible fungal infection" if "spots" in symptoms.lower() else "No severe disease detected"
        input_ref = symptoms

    save_advisory("disease", input_ref, diagnosis)
    simulate_sms_alert(session.get("username", "farmer"), f"Disease advisory: {diagnosis}")
    return jsonify({"disease_result": diagnosis})


@app.route("/irrigation", methods=["POST"])
@login_required
def irrigation():
    temp = float(request.form.get("temperature", 30))
    humidity = float(request.form.get("humidity", 50))
    rainfall = float(request.form.get("rainfall", 0))
    advice = irrigation_advice(temp, humidity, rainfall)

    save_advisory("irrigation", f"temp={temp},humidity={humidity},rainfall={rainfall}", advice)
    return jsonify({"irrigation_advice": advice})


@app.route("/market", methods=["POST"])
@login_required
def market_prediction():
    crop = request.form.get("crop", "wheat").lower()
    month = int(request.form.get("month", datetime.utcnow().month))
    rainfall = float(request.form.get("rainfall", 10))
    fuel_cost = float(request.form.get("fuel_cost", 280))

    predicted = predict_market_price(price_model, crop, month, rainfall, fuel_cost)
    result = f"Predicted {crop} price: PKR {predicted:.2f} per 40kg"

    save_advisory("market", f"crop={crop},month={month},rainfall={rainfall},fuel={fuel_cost}", result)
    return jsonify({"prediction": result})


@app.route("/api/weather")
@login_required
def weather_api():
    city = request.args.get("city", "Lahore")
    return jsonify(fetch_weather(city))


def save_advisory(advisory_type, input_data, result):
    db = get_db()
    db.execute(
        "INSERT INTO advisories (user_id, advisory_type, input_data, result, created_at) VALUES (?, ?, ?, ?, ?)",
        (
            session.get("user_id"),
            advisory_type,
            input_data,
            result,
            datetime.utcnow().isoformat(timespec="seconds"),
        ),
    )
    db.commit()
    logger.info("Advisory saved: %s", advisory_type)


@app.context_processor
def inject_language_data():
    dictionary = {
        "en": {
            "title": "Smart Agriculture Advisory System",
            "dashboard": "Dashboard",
            "logout": "Logout",
        },
        "ur": {
            "title": "سمارٹ زرعی مشاورتی نظام",
            "dashboard": "ڈیش بورڈ",
            "logout": "لاگ آؤٹ",
        },
    }
    return {"ui_text": dictionary.get(g.get("lang", "en"), dictionary["en"]), "lang": g.get("lang", "en")}


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
