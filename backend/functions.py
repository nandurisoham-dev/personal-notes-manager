from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, timedelta, timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

DB_PATH = "notes.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime, default = datetime.now())

class Notes(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default = datetime.now())

Base.metadata.create_all(engine)


def get_notes(user_id):
    session = Session(engine)
    notes = session.query(Notes).filter(Notes.user_id == user_id).all()
    response = []
    for note in notes:
        response.append(note)

    return {"code": 200 , "notes":response}


def notes_to_dict(note : Notes):
    return {
        "id" : note.id,
        "user_id" : note.user_id,
        "title" : note.title,
        "content" : note.content,
        "created_at" : note.created_at
    }
