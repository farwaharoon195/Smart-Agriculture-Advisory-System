import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_PORT = int(os.getenv("APP_PORT", "8000"))
    POSTGRES_URI = os.getenv("POSTGRES_URI", "sqlite:///smart_agri.db")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB = os.getenv("MONGO_DB", "smart_agri")
