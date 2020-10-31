import React from 'react';
import { Button, Form, FormGroup, Label, Input, Alert, Jumbotron } from 'reactstrap';
import axios from 'axios';
import { Redirect } from 'react-router-dom';

export default class Login extends React.Component {

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
        const data = {
            "email": e.target.email.value, 
            "password": e.target.password.value
        }

        const headers = {
            'Content-Type': 'application/json'
        }

        axios.post('login', data, { headers: headers })
        .then(
            res => {
                localStorage.setItem('token', res.data.token);
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
    }

    render() {
        if ( this.state.isLogin ){
            return <Redirect to = '/' />;
        }

        let loginErrorMssg = null;
        if ( this.state.loginError ) {
            loginErrorMssg = <Alert color = 'danger'> Login Failure! </Alert>
        }

        return (
            <div>
                <Jumbotron>
                <h1 className="display-3">Login</h1>
                <p className="lead">Enter your email id and password and submit to login.</p>
                <hr className="my-2" />
                    <Form onSubmit = { this.handleSubmit } >
                        <FormGroup>
                            <Label for="exampleEmail">Email</Label>
                            <Input type="text" name="email" id="exampleEmail" placeholder="with a placeholder" />
                        </FormGroup>
                        <FormGroup>
                            <Label for="examplePassword">Password</Label>
                            <Input type="password" name="password" id="examplePassword" placeholder="password placeholder" />
                        </FormGroup>
                        <Button>Submit</Button>
                        <Button href="/register" color="link">Register</Button>
                        {loginErrorMssg}
                    </Form>
                </Jumbotron>
            </div>
        )
    }
}
