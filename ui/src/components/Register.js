import React from 'react';
import { Button, Form, FormGroup, Label, Input, Alert, Jumbotron } from 'reactstrap';
import axios from 'axios';
import { Redirect } from 'react-router-dom';

export default class Register extends React.Component {

    constructor(){
        super();
        this.state = {
            isLogin : false,
            loginError : false 
        }
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleSubmit(e) {
        e.preventDefault();

        if ( e.target.password.value === e.target.cpassword.value ) {
        const data = {
            "name": e.target.name.value,
            "email": e.target.email.value, 
            "password": e.target.password.value
        }

        const headers = {
            'Content-Type': 'application/json'
        }

        axios.post('http://127.0.0.1:8080/createuser', data, { headers: headers })
        .then(
            res => {
                console.log('Successfully created user.')
                this.setState({
                    isLogin : true
                })
            }
        )
        .catch(
            err => {
                console.log(err)
                this.setState({
                    loginError : true
                })
            }
        )
        } else {
            console.log('Your password doesnot match confirm password.')
            this.setState({
                loginError : true
            })
        }
    }

    render() {
        if ( this.state.isLogin ){
            return <Redirect to = '/login' />;
        }

        let loginErrorMssg = null;
        if ( this.state.loginError ) {
            loginErrorMssg = <Alert color = 'danger'> Registration Failure! </Alert>
        }

        return (
            <div>
                <Jumbotron>
                <h1 className="display-3">Register</h1>
                <p className="lead">Enter all mandatory details and submit for registration.</p>
                <hr className="my-2" />
                
                <Form onSubmit = { this.handleSubmit } >
                    <FormGroup>
                        <Label for="name">Name</Label>
                        <Input type="text" name="name" id="name" placeholder="Your full name..." />
                    </FormGroup>
                    <FormGroup>
                        <Label for="email">Email</Label>
                        <Input type="email" name="email" id="email" placeholder="Your valid email..." />
                    </FormGroup>
                    <FormGroup>
                        <Label for="password">Password</Label>
                        <Input type="password" name="password" id="password" />
                    </FormGroup>
                    <FormGroup>
                        <Label for="cpassword">Confirm Password</Label>
                        <Input type="password" name="cpassword" id="cpassword" />
                    </FormGroup>
                    <Button>Submit</Button>
                    {loginErrorMssg}
                </Form>
                </Jumbotron>
            </div>
        )
    }
}
