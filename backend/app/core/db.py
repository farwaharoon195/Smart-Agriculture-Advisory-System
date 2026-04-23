from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pymongo import MongoClient

Base = declarative_base()
SessionLocal = None
mongo_client = None
mongo_db = None


def init_postgres(app):
    global SessionLocal
    from app import models  # ensure model metadata is registered
    engine = create_engine(app.config["POSTGRES_URI"], echo=False)
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)


def init_mongo(app):
    global mongo_client, mongo_db
    mongo_client = MongoClient(app.config["MONGO_URI"])
    mongo_db = mongo_client[app.config["MONGO_DB"]]
