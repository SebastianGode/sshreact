import React from 'react';
import { Switch, Route } from 'react-router-dom';

import Register from './Register';
import Login from './Login';
import Verify from './Verify';
import Sshclient from './Sshclient';
import Account from './Account';

const Main = () => {
  return (
    <Switch>
      <Route exact path='/' component={Register}></Route>
      <Route exact path='/login' component={Login}></Route>
      <Route exact path='/verify' component={Verify}></Route>
      <Route exact path='/sshclient' component={Sshclient}></Route>
      <Route exact path='/account' component={Account}></Route>
    </Switch>
  );
}

export default Main;