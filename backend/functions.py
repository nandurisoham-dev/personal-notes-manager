from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base, session
from datetime import datetime, timedelta, timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

DB_PATH = "notes.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


ACCESS_TOKEN_EXPIRY = 15
REFRESH_TOKEN_EXPIRY = 7 * 24 * 60
SECRET_KEY ="SECRET123"
ALGORITHM = "HS256"


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
        response.append(notes_to_dict(note))
    session.close()

    return {"code": 200 , "notes":response}


def create_note(user_id , title , content):
    session = Session(engine)
    note = Notes(user_id=user_id , title=title , content=content)
    session.add(note)
    session.commit()
    response = notes_to_dict(note)
    session.close()
    return {"code": 200 , "notes":response}




def notes_to_dict(note : Notes):
    return {
        "id" : note.id,
        "user_id" : note.user_id,
        "title" : note.title,
        "content" : note.content,
        "created_at" : note.created_at
    }
def verify_login(username, password):
    session = Session(engine)
    user = session.query(Users).filter_by(user_name = username).first()
    if user is None:
        session.close()
        return False
    try:
        ph.verify(user.password,password)
    except VerifyMismatchError:
        session.close()
        return False
    if user.user_type:
        user_type = user.user_type
    else:
        user_type = "user"
    session.close()
    access_token = create_token(username=username, token_type="access",user_type=user_type)
    refresh_token = create_token(username=username, token_type="refresh",user_type=user_type)
    return {"access_token": access_token, "refresh_token": refresh_token}

def create_token(username, token_type,user_type="user"):
    payload = {
        "username": username,
        'token_type': token_type,
        'user_type': user_type,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY if token_type == "access" else REFRESH_TOKEN_EXPIRY)  # turnery expression
    }
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return token



def verify_token(token,token_type):
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return False
    if payload["token_type"] == token_type:
        return payload
    return False

#--------- Users -----------

def register_user(user_name:str,password:str,user_type:str="user"):
    session = Session(engine)
    user_exists = session.query(Users).filter_by(user_name=user_name).first()
    if user_exists is not None:
        session.close()
        return False
    session.add(Users(user_name=user_name,password=ph.hash(password),user_type=user_type))
    session.commit()
    session.close()
    return True

