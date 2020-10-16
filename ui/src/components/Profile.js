import React from 'react';
import axios from 'axios';
import Unauthorized from './Unauthorized';
import { Col, 
        Container, 
        Row, 
        Toast, 
        ToastBody, 
        ToastHeader, 
        Button,
        Form, 
        FormGroup,
        Input,
        Label } from 'reactstrap';
import InternalError from './InternalError';

class Profile extends React.Component {

    constructor(){
        super();
        this.state = {
            loggedin : "no",
            error : "no"
        }
        this.handleExamCountUpdate = this.handleExamCountUpdate.bind(this)
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

            axios.get('http://127.0.0.1:8080/user', header)
            .then(
                res => {
                    this.setState({
                        userid: res.data.userid,
                        user: res.data.name,
                        email: res.data.email,
                        examcount: res.data.examcount,
                        hasRequest: res.data.isexamcountupdate,
                        loggedin: "yes",
                        error: "no" 
                    })
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

    handleExamCountUpdate(e) {
        if ( localStorage.getItem('token') === null ) {
            console.log('No token!!!')
            this.setState({
                loggedin: "no",
                error: "no"
            })
        } else if ( isNaN(parseInt(e.target.examcount.value)) ) {
            console.log('Not good value inputed!')
            this.setState({
                loggedin: "yes",
                error: "yes"
            })
        } else {
            const header = {
                headers : {
                    'Content-Type': 'application/json',
                    token : localStorage.getItem('token')
                }            
            }   

            const data = {
                "examcount": parseInt(e.target.examcount.value)
            }   

            axios.post('http://127.0.0.1:8080/updateexamcount', data, header)
            .then(
                res => {
                    console.log(res);
                    this.setState({
                        updateheader : 'Succesfully updated exam count!',
                        updateHeaderType : 'success',
                        loggedin: "yes",
                        error: "no"                        
                    })
                }
            ).catch(
                err => {
                    console.log(err);
                    this.setState({
                        updateheader : 'Failed updated exam count!',
                        updateHeaderType : 'failure',
                        loggedin: "yes",
                        error: "yes"
                    })
                }
            )
        }
        console.log(this.state)
    }

    render () {

        let echeader =  <ToastHeader icon="success">
                            Available Exam Count:
                        </ToastHeader>
        
        if ( this.state.examcount < 1 ){
            echeader =  <ToastHeader icon="danger">
                            Available Exam Count:
                        </ToastHeader>
        }

        let addExamButton = <Button outline color="success" >Request</Button>
        if ( this.state.hasRequest == 1 ){
            addExamButton = <Button disabled="true" >Request</Button>
        }

        let adminComponent = null ;
        if ( this.state.userid === 0 ) {
            adminComponent = <Row>
                                <Col sm='12' md={{ size: 6, offset: 3 }}>
                                    <Toast>
                                        <ToastHeader>
                                            Approve ExamCount Request:
                                        </ToastHeader>
                                        <ToastBody>
                                            <Button href="/approvepage" outline color="danger">Approval Page</Button>
                                        </ToastBody>
                                    </Toast>
                                </Col>
                            </Row>
        } 

        if ( this.state.loggedin === "no" ) {
            return <Unauthorized />
        } else if ( this.state.error === "yes" ) {
            return <InternalError/>
        } else {
            return (
                <Container>
                    <Row>
                        <Col><br></br></Col>
                    </Row>
                    <Row>
                        <Col sm='12' md={{ size: 6, offset: 3 }}>
                            <Toast>
                                <ToastHeader>
                                    Name:
                                </ToastHeader>
                                <ToastBody>
                                    {this.state.user}
                                </ToastBody>
                            </Toast>
                        </Col>
                    </Row>
                    <Row>
                        <Col><br></br></Col>
                    </Row>
                    <Row>
                        <Col sm='12' md={{ size: 6, offset: 3 }}>
                            <Toast>
                                <ToastHeader>
                                    Email:
                                </ToastHeader>
                                <ToastBody>
                                    {this.state.email}
                                </ToastBody>
                            </Toast>
                        </Col>
                    </Row>
                    <Row>
                        <Col><br></br></Col>
                    </Row>
                    <Row>
                        <Col sm='12' md={{ size: 6, offset: 3 }}>
                            <Toast>
                                {echeader}                                
                                <ToastBody>
                                    {this.state.examcount}
                                </ToastBody>
                            </Toast>
                        </Col>
                    </Row>
                    <Row>
                        <Col><br></br></Col>
                    </Row>
                    <Row>
                        <Col sm='12' md={{ size: 6, offset: 3 }}>
                            <Toast>
                                <ToastHeader>
                                    Add Exam:
                                </ToastHeader>
                                <ToastBody>
                                    <Form onSubmit = {this.handleExamCountUpdate}>
                                        <Row form>
                                        <Col md={6}>
                                            <FormGroup>
                                            <Label for="examcount">Count</Label>
                                            <Input type="text" name="examcount" id="examcount" />
                                            </FormGroup>
                                        </Col>
                                        </Row>
                                        {addExamButton}
                                    </Form>                                    
                                </ToastBody>
                            </Toast>
                        </Col>
                    </Row>
                    <Row>
                        <Col><br></br></Col>
                    </Row>
                    <Row>
                        <Col sm='12' md={{ size: 6, offset: 3 }}>
                            <Toast>
                                <ToastHeader>
                                    Update Password:
                                </ToastHeader>
                                <ToastBody>
                                    <Button href="/updatepassword" outline color="danger">Update Page</Button>
                                </ToastBody>
                            </Toast>
                        </Col>
                    </Row>
                    <Row>
                        <Col><br></br></Col>
                    </Row>
                    {adminComponent}
                </Container>
            )
        }
    }
}


export default Profile;
