import React, {useEffect, useState} from 'react';
import axios from 'axios';
import { ScaleButton } from '@telekom/scale-components-react';

function Account() {
  const Content = () => {
      const [content, setContent] = useState("");
      useEffect(() => {
          const jsontoken = {
            "verify": {
              "token": sessionStorage.getItem('token')
            }
          }
          setContent(
            <h1>Checking Token...</h1>
          )
          axios.post('/api/verifylogin', jsontoken)
              .then((response) => {
                setContent(
                    <div class="centered">
                        <h3>Do you want to delete your account?</h3>
                        <ScaleButton type="button" id="del-btn">Delete Account</ScaleButton>
                    </div>
                )
                document.getElementById("del-btn").addEventListener("click", function(){
                    setContent(
                        <div class="centered">
                            <h3>Deleting account...</h3>
                        </div>
                    )
                    axios.post('/api/deleteaccount', jsontoken)
                        .then((response) => {
                            alert("Account successfully deleted")
                            window.location.replace("/");
                        })
                        .catch((reason) => {
                            alert("Something went wrong")
                        })
                }, false);
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
