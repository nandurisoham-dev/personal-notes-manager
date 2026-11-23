import NoteCard from "./NoteCard.jsx";

function Notes({notes}){
    return <>
        {notes.map((note) => <NoteCard id={note.title} title={note.title} content={note.content} createdAt={note.createdAt}/>)}
    </>
}

export default Notes