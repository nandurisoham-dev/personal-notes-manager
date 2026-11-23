import {useState} from "react";
import {Navigate} from "react-router";
const API_URL = "http://localhost:8001"

function Register(){
      const [username, setUsername] = useState("");
      const [password, setPassword] = useState("");
      const [userType, setUserType] = useState("");
      const [registered, setRegistered] = useState(false);

      function handleUser(e) {    // function is an event handler used to update the component's state whenever someone types into the input field
         setUsername(e.target.value);

      }
      function handlePass(e) {    // function is an event handler used to update the component's state whenever someone types into the input field
         setPassword(e.target.value);

      }
      function handleType(e) {    // function is an event handler used to update the component's state whenever someone types into the input field
         setUserType(e.target.value);
      }

      function register(username , password,user_type){

          fetch(API_URL + "/register", {
              method : 'POST',
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                  "username":username,
                  "password":password,
                  "user_type":user_type
              }),
          })
            .then((response) =>{if (response.ok){setRegistered(true)} return response.json()})

      }

      function handleSubmit(e) {
        e.preventDefault(); // Prevents the page from refreshing on form submit
         // Pass the current RollNo state up to the parent component
        register(username,password,userType);


      }
      if (registered){
          return <Navigate replace to="/login" />;
      }
    return (

        <form className="inline-form" onSubmit={handleSubmit}>
          <label className="field">Enter your Username:
            <input
              type="text"
              value={username}
              onChange={handleUser}
            />
          </label>
            <label className="field">Enter your password:
            <input
              type="password"
              value={password}
              onChange={handlePass}
            />
          </label>
            <label className="filter">Type:

            <select name="type" value={userType} onChange={handleType}>
                <option value="dispatch">Dispatch</option>
                <option value="package">Package</option>
            </select>
            </label>
          <button type='submit'>Register</button>
        </form>
    )

}


export default Register