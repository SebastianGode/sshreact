import React, {useEffect, useState} from 'react';
import axios from 'axios';

function Account() {
  const Content = () => {
      const [content, setContent] = useState("");
      useEffect(() => {
          const urlParams = new URLSearchParams(window.location.search)
          const jsontoken = {
            "verify": {
              "token": urlParams.get('token')
            }
          }
          setContent(
            <h1>Checking Token...</h1>
          )
          axios.post('/api/verifylogin', jsontoken)
              .then((response) => {
                setContent(
                  <h1>Verification successful!</h1>
                )
              })
              .catch((reason) => {
                console.log(reason.response.data)
                setContent(
                  <h1>You need to sign-in first! Redirecting...</h1>
                )
                setTimeout(() => {
                    window.location.replace("/login");
                  }, 1000)
              })
      }, [])
      return content
    }
  return (
    <div class="centered">
      <Content/>
    </div> 
  );
}

export default Account;
