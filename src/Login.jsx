import React, {useState, useEffect} from 'react';
import axios from 'axios';
import { useHistory } from 'react-router-dom';
import { ScaleTextField, ScaleButton } from '@telekom/scale-components-react';

function sha512(str) {
  return crypto.subtle.digest("SHA-512", new TextEncoder("utf-8").encode(str)).then(buf => {
    return Array.prototype.map.call(new Uint8Array(buf), x=>(('00'+x.toString(16)).slice(-2))).join('');
  });
}


function Login() {  
  const [email, setEmail] = useState('');
  const handleEmailChange = event => {
    setEmail(event.target.value)
  };

  const [password1, setPassword1] = useState('');
  const handlePassword1Change = event => {
    setPassword1(event.target.value)
  };

  if (sessionStorage.getItem('token') != null) {
    const verifyjson = {
      "verify": {
        "token": sessionStorage.getItem('token')
      }
    }
    axios.post('/api/verifylogin', verifyjson)
        .then((response) => {
          window.location.replace("/sshclient");
        })
        .catch((reason) => {
          console.log("Token invalid, please login again")
          sessionStorage.removeItem('token')
        })
  }
  const handleSubmit = event => {
    event.preventDefault();
    sha512(`${password1}`).then((hashedpw) => {
      const loginjson = {
        "auth": {
          "email": `${email}`,
          "password": hashedpw
        }
      }
      axios.post('/api/login', loginjson)
        .then((response) => {
          sessionStorage.setItem('token', response.data.verification.token)
          window.location.replace("/sshclient");
        })
        .catch((reason) => {
          alert(reason.response.data.verification.error)
        })
      
    })

    
  };

  return (
    <div>
      <form action="action_page.php" onSubmit={handleSubmit}>
        <div class="container">
          <h1 class="Sign-Up">Log-In</h1>
          <p>Please fill in this form to Log-In into your account.</p>
          
          <ScaleTextField label="E-Mail" required name="email" onScaleChange={handleEmailChange} value={email}></ScaleTextField>
          <p></p>
          <ScaleTextField label="Password" type="password" name="password1" onScaleChange={handlePassword1Change} value={password1} required></ScaleTextField>
          <p></p>
          <ScaleButton type="submit">Log-In</ScaleButton>
        </div>
      </form>
    </div> 
  );
}

export default Login;
