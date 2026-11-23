import { useState , useEffect } from 'react'
import './App.css'
import Main from "./pages/Main.jsx";

const API_URL = "http://localhost:8001"
function App() {
  const [notes,setNotes] = useState([])
  const [token , setToken] = useState("")

  function updateNotes(){
      fetch(API_URL + "/packages" , {
          headers : {
              'token' : token
          }
      })
        .then((response) => response.json())
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
        <Route path="/" element={<Main token={token} notes={notes}/>} />

        <Route path="*" element={<h1>404 Not Found</h1>} />
    </Routes>
    </>
  )
}

export default App
