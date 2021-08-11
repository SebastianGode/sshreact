import React from 'react';
import { Switch, Route } from 'react-router-dom';

import Register from './Register';
import Login from './Login';

const Main = () => {
  return (
    <Switch>
      <Route exact path='/' component={Register}></Route>
      <Route exact path='/login' component={Login}></Route>
    </Switch>
  );
}

export default Main;