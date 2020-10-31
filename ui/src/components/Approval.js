import React from 'react';
import { Button, Form, FormGroup, Label, Input, Alert, Jumbotron } from 'reactstrap';
import axios from 'axios';
import { Redirect } from 'react-router-dom';

export default class Approval extends React.Component {

    constructor(){
        super();
        this.state = {
            completeApproval : false,
            updateError : false 
        }
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleSubmit(e) {
        e.preventDefault();
        console.log(e.target.userid.value);
        console.log(e.target.examcount.value);
        if ( localStorage.getItem('token') === null ) {
            console.log('No token!!!')
            this.setState({
                completeApproval: false,
                updateError: true
            })
        } else if ( isNaN(parseInt(e.target.examcount.value)) === false ) {  

            const headers = {
                token : localStorage.getItem('token')
            }   

            let urlString = 'applyexamcount/'+
            e.target.userid.value + '/' +
            e.target.examcount.value

            console.log(urlString)

            axios.get(urlString, { headers: headers })
            .then(
                res => {
                    this.setState({
                        completeApproval: true,
                        updateError: false
                    })
                }
            )
            .catch(
                err => {
                    console.log(err)
                    this.setState({
                        completeApproval: false,
                        updateError: true
                    })
                }
            )
        } else {
            console.log('Your password doesnot match confirm password.')
            this.setState({
                completeApproval: false,
                updateError: true
            })
        }
    }

    render() {
        if ( this.state.completeApproval ){
            return <Redirect to = '/' />;
        }

        let updateErrorMssg = null;
        if ( this.state.updateError ) {
            updateErrorMssg = <Alert color = 'danger'> Approval Failure! </Alert>
        }

        return (
            <div>
                <Jumbotron>
                <h1 className="display-3">Aprrovals</h1>
                <p className="lead">Enter userid and updated exam count to approve exam count request.</p>
                <hr className="my-2" />
                    <Form onSubmit = { this.handleSubmit } >
                        <FormGroup>
                            <Label for="userid">User Id</Label>
                            <Input type="text" name="userid" id="userid" />
                        </FormGroup>
                        <FormGroup>
                            <Label for="examcount">Exam Count</Label>
                            <Input type="text" name="examcount" id="examcount" />
                        </FormGroup>
                        <Button>Submit</Button>
                        {updateErrorMssg}
                    </Form>
                </Jumbotron>
            </div>
        )
    }
}
