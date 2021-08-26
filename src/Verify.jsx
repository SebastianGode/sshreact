import React, {useEffect, useState} from 'react';
import axios from 'axios';

function Verify() {
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
          axios.post('/api/verify', jsontoken)
              .then((response) => {
                setContent(
                  <h1>Verification successful! You will be redirected in 5 seconds.</h1>
                )
                setTimeout(() => {
                  window.location.replace("/login");   
                }, 5000)
              })
              .catch((reason) => {
                console.log(reason.response.data)
                setContent(
                  <h1>Error occured</h1>
                )
                setTimeout(() => {
                  alert(reason.response.data.verification.error)
                  window.location.replace("/");
                }, 400)
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

export default Verify;
