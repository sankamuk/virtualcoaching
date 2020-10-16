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
import Register from './components/Register';
import Approval from './components/Approval';
import Footer from './components/Footer';
import Query from './components/Query';


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
          <Route path = '/register' component = {Register} />
          <Route path = '/approvepage' component = {Approval} />
          <Route path = '/query' component = {Query} />
          <Route path = '/updatepassword' component = {UpdatePassword} />
          <Route component = {ErrorPage} />
        </Switch>
        <Footer/>
      </div>
    </BrowserRouter>
  );
}

export default App;
