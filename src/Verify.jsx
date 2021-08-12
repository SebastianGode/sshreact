import React, {useState, useEffect} from 'react';

function Verify() {
    const urlParams = new URLSearchParams(window.location.search)
    const token = urlParams.get('token')
    console.log(token)

  return (
    <div>
      
    </div> 
  );
}

export default Verify;
