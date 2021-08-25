import React, {useEffect, useState} from 'react';
import axios from 'axios';
import { wait } from '@testing-library/react';

function Sshclient() {  

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
                setContent(
                  <div class="centered">
                    <h1>Creating an Server instance for you, please wait...</h1>
                  </div>
                )
                const instancejson = {
                  "verify": {
                    "token": sessionStorage.getItem('token')
                  }
                }
                axios.post('/api/createinstance', instancejson)
                    .then((response) => {
                      console.log(response.data)
                      setTimeout(() => {  
                          // Download function in order to download the private key file
                          function download(filename, text) {
                            var element = document.createElement('a');
                            element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
                            element.setAttribute('download', filename);
                        
                            element.style.display = 'none';
                            document.body.appendChild(element);
                        
                            element.click();
                        
                            document.body.removeChild(element);
                          }
                          const linktosshclient = ("https://ssh.otc.ddnss.org/#+SSH:ubuntu@" + response.data.floating_ip + "%7CPrivate%20Key%7Cutf-8")
                          setContent(
                            <div class="centered">
                              <h1>Server instance created</h1>
                              <p>IP: {response.data.floating_ip}</p>
                              <p>username: ubuntu</p>
                              <input type="button" id="dwn-btn" value="Download private-key file"/>
                              <p></p>
                              <p>You can now connect to this instance through ssh using the private key for authentication</p>
                              <p>Either use your preferred ssh client or try our online In-Browser client: <a href={linktosshclient} target="_blank">Link</a></p>
                            </div>
                          )
                          document.getElementById("dwn-btn").addEventListener("click", function(){
                              // Generate download of private key file with some content
                              var text = response.data.private_key
                              var filename = (response.data.name + ".privatekey");
                              
                              download(filename, text);
                          }, false);
                       }, 25000);
                      
                      
                    })
                    .catch((reason) => {
                      console.log(reason.response)
                      sessionStorage.removeItem('token')
                      setContent("Authentication error!")
                      // window.location.replace("/login");
                    })
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
