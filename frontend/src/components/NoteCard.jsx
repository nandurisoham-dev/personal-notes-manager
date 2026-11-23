function NoteCard({title,content, createdAt}){

    return <>
        <h2>{title}</h2>
        <p>{content}</p>
        <br/>
        <p>created At: {createdAt}</p>
    </>

}

export default NoteCard