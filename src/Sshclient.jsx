import React, {useEffect, useState} from 'react';
import axios from 'axios';


function Sshclient() {  
  var isLoaded = false

  const Content = () => {
    const [content, setContent] = useState("");
    useEffect(() => {
      switch (sessionStorage.getItem('token')) {
        case null:
          setContent("You are not logged in!")
          // window.location.replace("/login");
        default:
          const verifyjson = {
            "verify": {
              "token": sessionStorage.getItem('token')
            }
          }
          axios.post('/api/verifylogin', verifyjson)
              .then((response) => {
                console.log(response.data.verification)
                isLoaded = true
                const test="test"
                setContent(
                  <div>
                    <h1>test {test}</h1>
                  </div>
                )
              })
              .catch((reason) => {
                console.log(reason.response)
                sessionStorage.removeItem('token')
                setContent("You are not logged in!")
                // window.location.replace("/login");
              })
      }
    }, [])
    return content
  }
  
  return (
    <div>
      <Content/>
    </div>
  )
  
}

export default Sshclient;
