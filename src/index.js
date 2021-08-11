import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Main from './Main.jsx';
import NavBar from './Navbar';
import Footer from './Footer.jsx';
import reportWebVitals from './reportWebVitals';
import '@telekom/scale-components/dist/scale-components/scale-components.css';
import {
    applyPolyfills,
    defineCustomElements,
  } from '@telekom/scale-components/loader';
import { BrowserRouter } from 'react-router-dom';


applyPolyfills().then(() => {
    defineCustomElements(window);
});

ReactDOM.render(
    <BrowserRouter>

        <NavBar />
        <Main />
        
    </BrowserRouter>,
    
    document.getElementById('root')
)

// ReactDOM.render(
    
//     document.getElementById('root')
// );

ReactDOM.render(
    <Footer />,
    document.getElementById('footer')
)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
