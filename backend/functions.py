from sqlalchemy import Integer, String, Column, create_engine, DateTime
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, timedelta, timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

DB_PATH = "notes.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class users(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime, default = datetime.now())

class notes(base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, foreign_key(users.id))
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default = datetime.now())

Base.metadata.create_all(engine)