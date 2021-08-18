import React, {useEffect} from 'react';
import axios from 'axios';


function Sshclient() {  
  var isLoaded = false

  useEffect(() => {
    switch (sessionStorage.getItem('token')) {
      case null:
        window.location.replace("/login");
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
            })
            .catch((reason) => {
              console.log(reason.response)
              sessionStorage.removeItem('token')
              window.location.replace("/login");
            })
    }
  }, [])
  

  if (isLoaded === false) {
    return (
      <div>
        <h1>Test</h1>
      </div>
    )
  }
  return (
    <div>
      <h1>Test2</h1>
    </div>
  )
  
}

export default Sshclient;
