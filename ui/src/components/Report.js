import React, { Component } from 'react';
import axios from 'axios';
import { Col, Container, Jumbotron, Row, Table } from 'reactstrap';
import Unauthorized from './Unauthorized';
import InternalError from './InternalError';

export default class Report extends Component {

    constructor(){
        super();
        this.state = {
            exam_details : null,
            question_details : null,
            latest_exam : null,
            loggedin : "no",
            error : "no"
        }
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

            axios.get('http://127.0.0.1:8080/getreport', header)
            .then(
                res => {
                    this.setState({
                        exam_details : res.data.exam,
                        question_details : res.data.question,
                        latest_exam : res.data.latest,
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

    render() {

        if ( this.state.loggedin === "no" ) {
            return <Unauthorized />
        } else if ( this.state.error === "yes" ) {
            return <InternalError/>
        } else {
            let examdetails = null;
            if ( this.state.exam_details !== null ){
                examdetails =                     <Table striped>
                <tbody>
                <tr>
                <th scope="row"></th>
                <td>Total Examination</td>
                <td>{this.state.exam_details.totalexam}</td>
                </tr>
                <tr>
                <th scope="row"></th>
                <td>Passed Examination</td>
                <td>{this.state.exam_details.passedexam}</td>
                </tr>
                <tr>
                <th scope="row"></th>
                <td>Average Time</td>
                <td>{this.state.exam_details.avgtime}</td>
                </tr>
                <tr>
                <th scope="row"></th>
                <td>Maximum Time</td>
                <td>{this.state.exam_details.maxtime}</td>
                </tr>
                <tr>
                <th scope="row"></th>
                <td>Minimum Time</td>
                <td>{this.state.exam_details.mintime}</td>
                </tr>
                </tbody>
                </Table>
            }   


            let questionbody = null;
            if ( this.state.question_details !== null ){
                let qarr = this.state.question_details
                let id = null;
                questionbody = qarr.map( (v, i) => {
                    const { correctattempt, 
                                difficulty, 
                                reportquestionid,
                                subject,
                                totalattempt,
                                userid} = v
                    id = subject+difficulty;
                    return (
                        <tr key={id}>
                            <th scope="row"></th>
                            <td>{subject}</td>
                            <td>{difficulty}</td>
                            <td>{totalattempt}</td>
                            <td>{correctattempt}</td>
                        </tr>
                    )
                }   

                )
            }   

            let questiondetails = null;
            if ( this.state.latest_exam !== null ){
                questiondetails =   <Table striped>
                                        <thead>
                                            <tr>
                                            <th>#</th>
                                            <th>Subject</th>
                                            <th>Difficulty Level</th>
                                            <th>Total Question</th>
                                            <th>Correct Answer</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {questionbody}
                                        </tbody>
                                    </Table>
            }   


            let latestquestionrow = null;
            if ( this.state.latest_exam !== null ){
                let qlst = this.state.latest_exam.aggregate 

                latestquestionrow = Object.keys(qlst).map(function(k1, i1) {
                    return Object.keys(qlst[k1]).map(function(k2, i2) {
                        let id = k1+k2;
                        return (
                            <tr key={id}>
                                <th scope="row"></th>
                                <td >{k1}</td>
                                <td >{k2}</td>
                                <td >{qlst[k1][k2]['total']}</td>
                                <td >{qlst[k1][k2]['correct']}</td>
                            </tr>
                        )
                    })
                })
            }   

            let latestexamdetail = null ;
            if ( this.state.latest_exam !== null ){
                latestexamdetail =                     <Table striped>
                <tbody>
                <tr>
                <th scope="row"></th>
                <td>Final Status: {this.state.latest_exam.status}</td>
                </tr>
                <tr>
                <th scope="row"></th>
                <td>Percentage: {this.state.latest_exam.percentage}</td>
                </tr>
                <tr>
                <th scope="row"></th>
                <td>Start Time: {this.state.latest_exam.start}</td>
                </tr>
                <tr>
                <th scope="row"></th>
                <td>End Time: {this.state.latest_exam.end}</td>
                </tr>
                <tr>
                <th scope="row"></th>
                <td>Question Analysis</td>
                </tr>
                <tr>
                <th scope="row"></th>
                <td>
                    <Table dark>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Subject</th>
                                <th>Difficulty</th>
                                <th>Total</th>
                                <th>Success</th>
                            </tr>
                        </thead>
                        <tbody>
                            {latestquestionrow}
                        </tbody>
                    </Table>
                </td>
                </tr>
                </tbody>
                </Table>
            }   

            return (
                <Container>
                    <Row>
                        <Col><br></br></Col>
                    </Row>
                    <Row>
                        <Col sm='12' md={{ size: 6, offset: 3 }}>
                            <Jumbotron>
                            <h1 className="display-6">Exam History</h1>
                            {examdetails}
                            </Jumbotron>
                        </Col>
                        <Col sm='12' md={{ size: 6, offset: 0 }} >
                            <Jumbotron>
                            <h1 className="display-6">Latest Exam</h1>
                            {latestexamdetail}
                            </Jumbotron>
                        </Col>
                        <Col sm='12' md={{ size: 6, offset: 0 }} >
                            <Jumbotron>
                            <h1 className="display-6">Question History</h1>
                            {questiondetails}
                            </Jumbotron>
                        </Col>
                    </Row>
                </Container>
            )
        }
    }
}
