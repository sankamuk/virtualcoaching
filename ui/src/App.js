import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import Profile from './components/Profile';
import Navigation from './components/Navigation'
import Exam from './components/Exam';
import Report from './components/Report';
import Login from './components/Login';
import ErrorPage from './components/ErrorPage';
import Logout from './components/Logout';
import UpdatePassword from './components/UpdatePassword';


function App() {


  return (
    <BrowserRouter>
      <div>
        <Navigation />
        <Switch>
          <Route exact path = '/' component = {Profile} />
          <Route path = '/exam' component = {Exam} />
          <Route path = '/report' component = {Report} />
          <Route path = '/login' component = {Login} />
          <Route path = '/logout' component = {Logout} />
          <Route path = '/updatepassword' component = {UpdatePassword} />
          <Route component = {ErrorPage} />
        </Switch>
      </div>
    </BrowserRouter>
  );
}

export default App;
