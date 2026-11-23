import {useState} from "react";
import {Navigate} from "react-router";
import Notes from "../components/Notes.jsx";

function Main({token,notes}){

    if (token === ""){
          return <Navigate replace to="/login" />;
      }
    return (
    <>
      <Notes notes={notes}/>
    </>
  )
}

export default Main