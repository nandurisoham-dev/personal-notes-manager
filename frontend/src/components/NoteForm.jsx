import { useState , useEffect } from 'react'


function NoteForm({token,setNotes}){
    const [title,setTitle] = useState("")
    const [content,setContent] = useState("")

    function handleTitle(e) {    // function is an event handler used to update the component's state whenever someone types into the input field
        setTitle(e.target.value);
    }

    function handleContent(e) {    // function is an event handler used to update the component's state whenever someone types into the input field
        setContent(e.target.value);

    }

    function addNote(){
        fetch(API_URL + `/notes`, {
            method: "POST",
            headers: { "Content-Type": "application/json",'token' : token },
            body: JSON.stringify({
                  "title":title,
                  "content":content
                })
        })
            .then((response) => response.json())
            .then(() => {
                return fetch(API_URL + "/notes", {headers : {
              'token' : token
          }})

            })
            .then((response) => response.json())
            .then((data) => setNotes(data))
    }

    function handleSubmit(e) {
        e.preventDefault(); // Prevents the page from refreshing on form submit
        addNote()
    }

    return <>
        <form onSubmit={handleSubmit}>
            <label>Title:
                <input
                    type="text"
                    value={title}
                    onChange={handleTitle}
                />
            </label>
            <label>note:
                <textarea name="paragraph_text" cols="50" rows="10" value={content} onChange={handleContent}></textarea>
            </label>


            <button type='submit'>Add</button>
        </form>

    </>
}

export default NoteForm