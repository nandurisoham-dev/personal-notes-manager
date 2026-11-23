from os import access
from urllib import response

from fastapi import FastAPI, HTTPException, Body, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import functions

class Note(BaseModel):
    title: str
    content: str
app = FastAPI()
class UserRegister(BaseModel):
    username: str
    password: str
    email: str | None = None
class UserLogin(BaseModel):
    username: str
    password: str

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:5173"],
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.post("/register")
def register(user: UserRegister):
    created = functions.register_user(user_name=user.username, password=user.password, email=user.email)  # ADDED
    if not created:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: UserLogin):
    tokens = functions.verify_login(username=user.username, password=user.password)
    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return tokens

@app.get("/notes")
def get_all_notes(token = Header(None)):
    user_id = functions.verify_token(token=token, token_type="access")["user_id"]
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return functions.get_notes(user_id)["notes"]

@app.post("/notes")
def add_note(note : Note, token = Header(None)):
    user_id = functions.verify_token(token=token, token_type="access")["user_id"]
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return functions.create_note(user_id=user_id, title=note.title, content=note.content)