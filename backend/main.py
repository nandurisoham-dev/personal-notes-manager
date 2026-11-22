from urllib import response

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import functions

class Note(BaseModel):
    title: str
    content: str
app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:5173"],
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.get("/notes")
def get_all_notes( user_id : str):
    return functions.get_notes(user_id)["notes"]

@app.post("/notes")
def add_note(note : Note, user_id:str):
    return functions.create_note(user_id=user_id, title=note.title, content=note.content)