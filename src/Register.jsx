import React, {useState, useEffect} from 'react';
import axios from 'axios';
import { ScaleTextField, ScaleButton } from '@telekom/scale-components-react';

function sha512(str) {
  return crypto.subtle.digest("SHA-512", new TextEncoder("utf-8").encode(str)).then(buf => {
    return Array.prototype.map.call(new Uint8Array(buf), x=>(('00'+x.toString(16)).slice(-2))).join('');
  });
}


function Register() {
  const [currentTime, setCurrentTime] = useState(0);
  
  const [email, setEmail] = useState('');
  const handleEmailChange = event => {
    setEmail(event.target.value)
  };

  const [password1, setPassword1] = useState('');
  const handlePassword1Change = event => {
    setPassword1(event.target.value)
  };
  const [password2, setPassword2] = useState('');
  const handlePassword2Change = event => {
    setPassword2(event.target.value)
  };

  const handleSubmit = event => {
    event.preventDefault();
    if ((`${password1}`) === (`${password2}`)) {
      sha512(`${password1}`).then(hashedpw => {
        const jsonstring = {
          "auth": {
            "email": `${email}`,
            "password": hashedpw
          }
        }
        axios.post('/api/register', jsonstring)
            .then((response) => {
              alert("Please confirm your E-Mail adress now!")
              console.log(response.data.auth)
            })
            // .catch(reason => console.log(reason.response.data))
            .catch((reason) => {
              if (reason.response.data.error.errornumber === 1062) {
                alert("E-Mail address already registered!")
              }
              else {
                alert("An error occured.")
              }
            })
      });
    }
    else {
      alert('Passwords do not match!')
    }
  };

  return (
    <div>
      <form action="action_page.php" onSubmit={handleSubmit}>
        <div class="container">
          <h1 class="Sign-Up">Sign Up</h1>
          <p>Please fill in this form to create an account.</p>
          
          <ScaleTextField label="E-Mail" required name="email" onScaleChange={handleEmailChange} value={email}></ScaleTextField>
          <p></p>
          <ScaleTextField label="Password" type="password" name="password1" onScaleChange={handlePassword1Change} value={password1} required></ScaleTextField>
          <p></p>
          <ScaleTextField id="password2" label="Repeat Password" type="password" name="password2" onScaleChange={handlePassword2Change} value={password2} required></ScaleTextField>

          <p>By creating an account you agree to our <a href="https://open-telekom-cloud.com/en/data-protection" >Terms & Privacy</a>.</p>
          <ScaleButton type="submit">Register</ScaleButton>
        </div>
      </form>
    </div> 
  );
}

export default Register;
