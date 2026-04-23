from sqlalchemy import Column, Integer, String
from app.core.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    district = Column(String(100), nullable=False)
    preferred_language = Column(String(10), default="en")
