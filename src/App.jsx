import React from 'react';
import { ScaleTextField, ScaleButton } from '@telekom/scale-components-react';

function App() {
  return (
    <div>
      <form action="action_page.php">
        <div class="container">
          <h1 class="Sign-Up">Sign Up</h1>
          <p>Please fill in this form to create an account.</p>
          
          <ScaleTextField id="email" label="E-Mail" required></ScaleTextField>
          <p></p>
          <ScaleTextField id="password" label="Password" type="password" required></ScaleTextField>
          <p></p>
          <ScaleTextField id="passwordrepeat" label="Repeat Password" type="password" required></ScaleTextField>

          <p>By creating an account you agree to our <a href="#" >Terms & Privacy</a>.</p>
          <ScaleButton type="submit"> Register</ScaleButton>
        </div>
      </form>
    </div> 
  );
}

export default App;
