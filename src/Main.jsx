import React from 'react';
import { Switch, Route } from 'react-router-dom';

import Register from './Register';
import Login from './Login';
import Verify from './Verify';

const Main = () => {
  return (
    <Switch>
      <Route exact path='/' component={Register}></Route>
      <Route exact path='/login' component={Login}></Route>
      <Route exact path='/verify' component={Verify}></Route>
    </Switch>
  );
}

export default Main;