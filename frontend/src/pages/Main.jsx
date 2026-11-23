import {useState} from "react";
import {Navigate} from "react-router";
import Notes from "../components/Notes.jsx";
import NoteForm from "../components/NoteForm.jsx";

function Main({token,notes,updateToken, setNotes}){

    if (token === ""){
          return <Navigate replace to="/login" />;
      }
    return (
    <>
        <h1>Notes</h1>
      <Notes notes={notes}/>
        <h1>Add Note</h1>
        <NoteForm setNotes={setNotes} token={token} updateToken={updateToken}/>
    </>
  )
}

export default Main