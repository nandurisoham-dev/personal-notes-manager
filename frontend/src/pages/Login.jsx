import {useState} from "react";
import {Link, Navigate} from "react-router";

function Login({login,authed}){
      const [username, setUsername] = useState("");
      const [password, setPassword] = useState("");

      function handleUser(e) {
         setUsername(e.target.value);

      }
      function handlePass(e) {
         setPassword(e.target.value);

      }
      function handleSubmit(e) {
        e.preventDefault();
        login(username,password);


      }
      if (authed === true){
          return <Navigate replace to="/" />;
      }
    return (
        <>
            <h1>Login</h1>
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
          <button type='submit'>Login</button>
        </form>
        <nav>
          <Link to="/register">Register?</Link>
        </nav>
        </>

    )

}


export default Login