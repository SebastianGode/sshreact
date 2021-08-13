import React from 'react';
import axios from 'axios';

function Verify() {
    const urlParams = new URLSearchParams(window.location.search)
    const jsontoken = {
      "verify": {
        "token": urlParams.get('token')
      }
    }
    axios.post('/api/verify', jsontoken)
        .then((response) => {
          alert("Verification successful")
          window.location.replace("/login");   
        })
        .catch((reason) => {
          console.log(reason.response.data)
          alert(reason.response.data.verification.error)
          window.location.replace("/register");
        })
  return (
    <div>
      
    </div> 
  );
}

export default Verify;
