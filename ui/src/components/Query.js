import React from 'react';
import { Button, Form, FormGroup, Label, Input, Alert, Jumbotron } from 'reactstrap';
import axios from 'axios';

export default class Query extends React.Component {

    constructor(){
        super();
        this.state = {
            loginError : null 
        }
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleSubmit(e) {
        e.preventDefault();
        const data = {
            "email": e.target.email.value, 
            "query": e.target.query.value
        }

        const headers = {
            'Content-Type': 'application/json'
        }

        axios.post('query', data, { headers: headers })
        .then(
            res => {
                this.setState({
                    loginError : false
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
        console.log(this.state)
    }

    render() {

        let loginErrorMssg = null;
        if ( this.state.loginError === null ) {
            loginErrorMssg = null;
        } else if ( this.state.loginError === true ) {
            loginErrorMssg = <Alert color = 'danger'> Query Report Failure! </Alert>
        } else {
            loginErrorMssg = <Alert color = 'success'> Query Report Success! </Alert>
        }

        return (
            <div>
                <Jumbotron>
                <h1 className="display-3">Your Query</h1>
                <p className="lead">Note: You can only register one query at a time. After your query is answered you can register new query.</p>
                <hr className="my-2" />
                    <Form onSubmit = { this.handleSubmit } >
                        <FormGroup>
                            <Label for="email">Email</Label>
                            <Input type="email" name="email" id="email" placeholder="Your Email" />
                        </FormGroup>
                        <FormGroup>
                            <Label for="query">Query Text</Label>
                            <Input type="textarea" name="query" id="query" placeholder="Your Query. Max 100 Character." />
                        </FormGroup>
                        <Button>Submit</Button>
                        {loginErrorMssg}
                    </Form>
                </Jumbotron>
            </div>
        )
    }
}
