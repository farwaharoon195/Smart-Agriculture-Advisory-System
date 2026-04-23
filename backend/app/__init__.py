from flask import Flask
from flask_cors import CORS
from .core.config import Config
from .core.db import init_postgres, init_mongo
from .core.logging import configure_logging
from .api.routes import api_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    configure_logging(app)
    init_postgres(app)
    init_mongo(app)
    app.register_blueprint(api_bp, url_prefix="/api")
    return app
