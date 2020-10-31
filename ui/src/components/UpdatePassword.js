import React from 'react';
import { Button, Form, FormGroup, Label, Input, Alert } from 'reactstrap';
import axios from 'axios';
import { Redirect } from 'react-router-dom';

export default class UpdatePassword extends React.Component {

    constructor(){
        super();
        this.state = {
            isUpdate : false,
            updateError : false 
        }
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleSubmit(e) {
        e.preventDefault();
        if ( e.target.password.value === e.target.cpassword.value ) {
            const data = {
                "password": e.target.password.value
            }   

            const headers = {
                'Content-Type': 'application/json',
                token : localStorage.getItem('token')
            }   

            axios.post('updatepassword', data, { headers: headers })
            .then(
                res => {
                    localStorage.setItem('token', res.data.token);
                    this.setState({
                        isUpdate : true
                    })
                }
            )
            .catch(
                err => {
                    console.log(err)
                    this.setState({
                        updateError : true
                    })
                }
            )
        } else {
            console.log('Your password doesnot match confirm password.')
            this.setState({
                updateError : true
            })
        }
    }

    render() {
        if ( this.state.isUpdate ){
            return <Redirect to = '/login' />;
        }

        let passwordErrorMssg = null;
        if ( this.state.updateError ) {
            passwordErrorMssg = <Alert color = 'danger'> Update Password Failure! </Alert>
        }

        return (
            <div>
                <Form onSubmit = { this.handleSubmit } >
                    <FormGroup>
                        <Label for="password">Password</Label>
                        <Input type="password" name="password" id="password" />
                    </FormGroup>
                    <FormGroup>
                        <Label for="cpassword">Confirm Password</Label>
                        <Input type="password" name="cpassword" id="cpassword" />
                    </FormGroup>
                    <Button>Submit</Button>
                    {passwordErrorMssg}
                </Form>
            </div>
        )
    }
}
