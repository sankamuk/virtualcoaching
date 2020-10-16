import React, { Component } from 'react';
import axios from 'axios';
import { Table, Jumbotron, Button, Alert, FormGroup, Label, Col, Input, Form } from 'reactstrap';
import Unauthorized from './Unauthorized';
import InternalError from './InternalError';

export default class Exam extends Component {

    constructor(){
        super();
        this.state = {
            result : null,
            question : null,
            loggedin : "no",
            error : "no"
        }
        this.handleCreateExam = this.handleCreateExam.bind(this)
        this.handleQuestionSubmit = this.handleQuestionSubmit.bind(this)
    }

    handleCreateExam(e) {

        if ( localStorage.getItem('token') === null ) {
            console.log('No token!!!')
            this.setState({
                loggedin: "no",
                error: "no"
            })
        } else {
            const header = {
                headers : {
                    token : localStorage.getItem('token')
                }            
            }   

            axios.get('http://127.0.0.1:8080/createexam', header)
            .then(
                res => {
                    console.log(res);
                    this.setState({
                        loggedin: "yes",
                        error: "no"
                    })
                    window.location.reload();
                }
            ).catch(
                err => {
                    console.log(err);
                    this.setState({
                        loggedin: "yes",
                        error: "yes"
                    })
                }
            )
        }
        console.log(this.state) 
    }

    handleQuestionSubmit(e) {

        if ( localStorage.getItem('token') === null ) {
            console.log('No token!!!')
            this.setState({
                loggedin: "no",
                error: "no"
            })
        } else {

            const header = {
                headers : {
                    'Content-Type': 'application/json',
                    token : localStorage.getItem('token')
                }            
            }

            const data = {
                "choice": parseInt(e.target.option_selected.value)
            }

            axios.post('http://127.0.0.1:8080/submitanswer', data, header)
            .then(
                res => {
                    console.log(res);
                    this.setState({
                        loggedin: "yes",
                        error: "no"
                    })
                }
            ).catch(
                err => {
                    console.log(err);
                    this.setState({
                        loggedin: "yes",
                        error: "yes"
                    })
                }
            )
        }
        console.log(this.state) 

    }

    componentDidMount () {
        if ( localStorage.getItem('token') === null ) {
            console.log('No token!!!')
            this.setState({
                loggedin: "no",
                error: "no"
            })
        } else {
            const header = {
                headers : {
                    token : localStorage.getItem('token')
                }
            }

            axios.get('http://127.0.0.1:8080/userexam', header)
            .then(
                res => {
                    if ( typeof res.data.question !== "undefined" ) {
                        this.setState({
                            question : res.data.question,
                            option1 : res.data.option1,
                            option2 : res.data.option2,
                            option3 : res.data.option3,
                            option4 : res.data.option4,
                            loggedin: "yes",
                            error: "no"
                        })
                    } else if ( typeof res.data.result !== "undefined" ) {
                        this.setState({                        
                            result : res.data.result,
                            loggedin: "yes",
                            error: "no"
                        })
                    } else {
                        this.setState({                        
                            loggedin: "yes",
                            error: "no"
                        })
                    }
                }
            ).catch(
                err => {
                    console.log(err)
                    this.setState({
                        loggedin: "yes",
                        error: "yes"
                    })
                }
            )
        }
        console.log(this.state) 

    }

    render() {

        if ( this.state.loggedin === "no" ) {
            return <Unauthorized />
        } else if ( this.state.error === "yes" ) {
            return <InternalError/>
        } else if ( this.state.question !== null ) {
            return (
                <Jumbotron>
                <h1 className="display-3">Question</h1>
                <p className="lead">Choose an option an click submit to register your answer...</p>
                <hr className="my-2" />
                        <Form onSubmit = { this.handleQuestionSubmit }>
                            <FormGroup tag="fieldset" row>
                                <legend className="col-form-label col-md-6">
                                {this.state.question}
                                </legend>
                                <Col sm={10}>
                                <FormGroup check>
                                    <Label check>
                                    <Input  type="radio" 
                                            name="option_selected" 
                                            value="1"/>{' '}
                                    {this.state.option1}
                                    </Label>
                                </FormGroup>
                                <FormGroup check>
                                    <Label check>
                                    <Input  type="radio" 
                                            name="option_selected" 
                                            value="2"/>{' '}
                                    {this.state.option2}
                                    </Label>
                                </FormGroup>
                                <FormGroup check>
                                    <Label check>
                                    <Input  type="radio" 
                                            name="option_selected" 
                                            value="3"/>{' '}
                                    {this.state.option3}
                                    </Label>
                                </FormGroup>
                                <FormGroup check>
                                    <Label check>
                                    <Input  type="radio" 
                                            name="option_selected" 
                                            value="4"/>{' '}
                                    {this.state.option4}
                                    </Label>
                                </FormGroup>
                                </Col>
                            </FormGroup>
                            <Button outline color="primary" >Submit</Button>
                        </Form>
                </Jumbotron>
            )
        } else if ( this.state.result !== null ) {

            let exam_status =   <Alert color="success"> PASSES !!!
                                </Alert>
            
            if ( this.state.result.status === "FAILED" ) {
                exam_status = <Alert color="danger"> FAILED !!!
            </Alert>
            } 

            return (
                <Jumbotron>
                    <h1 className="display-3">Result</h1>
                    <p className="lead">
                        {exam_status}
                    </p>
                    <hr className="my-2" />
                    <p>
                    <Table striped>
                    <tbody>
                    <tr>
                    <th scope="row"></th>
                    <td>Percentage</td>
                    <td>{this.state.result.percentage}</td>
                    </tr>
                    <tr>
                    <th scope="row"></th>
                    <td>Start Time</td>
                    <td>{this.state.result.start}</td>
                    </tr>
                    <tr>
                    <th scope="row"></th>
                    <td>End Time</td>
                    <td>{this.state.result.end}</td>
                    </tr>
                    </tbody>
                    </Table>
                    </p>
                    <p className="lead">
                    <Button onClick = { this.handleCreateExam } color="primary">Start New Exam</Button>
                    </p>
                </Jumbotron>
            )
        } else {
            return (
            <Jumbotron>
               <h1 className="display-3">Sorry. Nothing for you!</h1>
               <p className="lead">You have no examination ongoing neither you have any examination history.</p>
               <hr className="my-2" />
               <p>Action: Schedule a new examination or go to profile page and request for examination if you have no examination quota.</p>
               <p className="lead">
                    <Button onClick = { this.handleCreateExam } color="primary">Start New Exam</Button>
               </p>
            </Jumbotron>
            )
        }
        
    }
}
