import { useState , useEffect } from 'react'
import './App.css'
import Main from "./pages/Main.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";


const API_URL = "http://localhost:8001"
function App() {
  const [notes,setNotes] = useState([])
  const [token , setToken] = useState("")
  const [refresh , setRefresh] = useState("")
  const [authed, setAuthed] = useState(false)

  function login(username , password){

      fetch(API_URL + "/login", {
          method : 'POST',
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
              "username":username,
              "password":password
          }),
      })
        .then((response) =>{if (response.ok){setAuthed(true)} return response.json()})
        .then((data) => {setToken(data.access_token) ; setRefresh(data.refresh_token)})



  }


  function updateToken(){
    fetch(API_URL + "/refresh" , {
          method : "POST",
          headers : {
              'token' : refresh
          }
      })
        .then((response) => response.json())
        .then((data) => setToken(data.access_token))
  }


  function updateNotes(){
      fetch(API_URL + "/notes" , {
          headers : {
              'token' : token
          }
      })
        .then((response) =>  { if (response.status === 401) {updateToken(); throw Error} return response.json()})
        .then((data) => setNotes(data))

  }

  useEffect(() => {
      if (token){
          updateNotes()
      }

  }, [token])


  return (
    <>
      <Routes>
        <Route path="/" element={<Main token={token} notes={notes} updateToken={updateToken} setNotes={setNotes}/>} />
        <Route path="/login" element={<Login login={login} authed={authed}/>} />
        <Route path="/register" element={<Register/>} />
        <Route path="*" element={<h1>404 Not Found</h1>} />
    </Routes>
    </>
  )
}

export default App
