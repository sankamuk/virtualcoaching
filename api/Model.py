from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import app
import json
import datetime

db = SQLAlchemy(app)

'''
------------------------------------------------
    Section: USER
------------------------------------------------ 
'''

class User(db.Model) :
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    examcount = db.Column(db.Integer, nullable=False)
    exams = db.relationship('Exam', backref='user', lazy=True)

    def json(self):
        if self :
            return {
                    'name': self.name,
                    'email': self.email,
                    'password': self.password,
                    'examcount': self.examcount,
                    'userid': self.userid            
            }
        else :
            return None

    def addUser( 
                _name, 
                _email, 
                _password) :
        new_user = User(name=_name, 
                        email=_email, 
                        password=_password,
                        examcount=0)
        db.session.add(new_user)

    def __repr__(self) :
        return json.dumps(
            {
                'name': self.name,
                'email': self.email,
                'password': self.password,
                'examcount': self.examcount,
                'userid': self.userid
            }
        )
    
    def getAllUser() :
        return [ User.json(user) for user in User.query.all() ]

    def getUserByEmail(_email) :
        return User.json(User.query.filter_by(email = _email).first())

    def getUserById(_id) :
        return User.json(User.query.filter_by(userid = _id).first())

    def deleteUserById(_id) :
        return User.query.filter_by(userid = _id).delete()

    def updateExamCountById(_id, _count) :
        user = User.query.filter_by(userid = _id).first()
        user.examcount = _count

    def updatePasswordId(_id, _password) :
        user = User.query.filter_by(userid = _id).first()
        user.password = _password        

    def commitSession() :
        db.session.commit()        

'''
------------------------------------------------
    Section: QUESTION
------------------------------------------------ 
'''   

class Question(db.Model) :
    __tablename__ = 'question'
    questionid = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(20), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    question = db.Column(db.String(60), nullable=False)
    option1 = db.Column(db.String(60))
    option2 = db.Column(db.String(60))
    option3 = db.Column(db.String(60))
    option4 = db.Column(db.String(60))
    answer = db.Column(db.Integer, nullable=False)
    examquestion = db.relationship('ExamQuestion', backref='Question', lazy=True)

    def json(self):
        if self :
            return {
                    'questionid': self.questionid,
                    'subject': self.subject,
                    'difficulty': self.difficulty,
                    'question': self.question,
                    'option1': self.option1,
                    'option2': self.option2,
                    'option3': self.option3,
                    'option4': self.option4,
                    'answer': self.answer              
            }
        else :
            return None

    def __repr__(self) :
        return json.dumps(
            {
                'questionid': self.questionid,
                'subject': self.subject,
                'difficulty': self.difficulty,
                'question': self.question,
                'option1': self.option1,
                'option2': self.option2,
                'option3': self.option3,
                'option4': self.option4,
                'answer': self.answer 
            }
        )

    def addQuestion(_subject, 
                    _difficulty, 
                    _question, 
                    _option1, 
                    _option2, 
                    _option3, 
                    _option4, 
                    _answer) :
        new_question = Question(
                        subject=_subject, 
                        difficulty=_difficulty, 
                        question=_question,
                        option1=_option1,
                        option2=_option2, 
                        option3=_option3, 
                        option4=_option4,
                        answer=_answer)
        db.session.add(new_question)

    def getQuestionById(_id) :
        return Question.json(Question.query.filter_by(questionid = _id).first())

    def getQuestionByCategory(_subject, _difficulty) :
        questionList = []
        for q in Question.query.filter_by(subject = _subject, difficulty = _difficulty) :
            questionList.append(Question.json(q))
        return [q['questionid'] for q in questionList]

    def commitSession() :
        db.session.commit()

'''
------------------------------------------------
    Section: EXAM
------------------------------------------------ 
''' 

class Exam(db.Model) :
    __tablename__ = 'exam'
    examid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    starttime = db.Column(db.DateTime, default=datetime.datetime.now())
    endtime = db.Column(db.DateTime)
    examquestion = db.relationship('ExamQuestion', backref='Exam', lazy=True)


    def json(self):
        if self :
            return {
                    'examid': self.examid,
                    'userid': self.userid,
                    'starttime': self.starttime,
                    'endtime': self.endtime          
            }
        else :
            return None 
    
    def __repr__(self) :
        return json.dumps(
            {
                'examid': self.examid,
                'userid': self.userid,
                'starttime': self.starttime,
                'endtime': self.endtime
            }
        )    

    def addExam(_userid) :
        new_exam = Exam(userid=_userid)
        db.session.add(new_exam)

    def getExamById(_examid) :
        return Exam.json(Exam.query.filter_by( examid = _examid ).first())

    def getActiveExamForUser(_userid) :
        for exam in Exam.query.filter_by( userid = _userid ) :
            if not exam.endtime :
                return exam.examid
        return None

    def getCompletedExamForUser(_userid) :
        examList = []
        for exam in Exam.query.filter_by( userid = _userid ) :
            if exam.endtime :
                examList.append(exam.examid)
        return examList

    def endExam(_examid) :
        exam = Exam.query.filter_by( examid = _examid ).first()
        exam.endtime = datetime.datetime.now()        

    def deleteExam(_examid) :
        Exam.query.filter_by( examid = _examid ).delete()

    def commitSession() :
        db.session.commit()        


'''
------------------------------------------------
    Section: EXAMQUESTION
------------------------------------------------ 
''' 

class ExamQuestion(db.Model) :
    __tablename__ = 'examquestion'
    examquestionid = db.Column(db.Integer, primary_key=True)
    examid = db.Column(db.Integer, db.ForeignKey('exam.examid'), nullable=False)
    questionid = db.Column(db.Integer, db.ForeignKey('question.questionid'), nullable=False)
    choice = db.Column(db.Integer)

    def json(self):
        if self :
            return {
                    'examquestionid': self.examquestionid,
                    'examid': self.examid,
                    'questionid': self.questionid,
                    'choice': self.choice          
            }
        else :
            return None 
    
    def __repr__(self) :
        return json.dumps(
            {
                'examquestionid': self.examquestionid,
                'examid': self.examid,
                'questionid': self.questionid,
                'choice': self.choice
            }
        )  

    def addExamQuestion(_examid, _questionid) :
        new_examquestion = ExamQuestion(examid=_examid, questionid=_questionid)
        db.session.add(new_examquestion)

    def getExamQuestion(_examid) :
        questionList = []
        for question in ExamQuestion.query.filter_by(examid = _examid) :
            questionList.append(ExamQuestion.json(question))
        return questionList

    def getUnansweredExamQuestion(_examid) :
        questionList = []
        for question in ExamQuestion.query.filter_by(examid = _examid) :
            if not question.choice :
                questionList.append(ExamQuestion.json(question))
        return questionList

    def setAnswerToQuestion(_examquestionid, _choice) :
        examquestion = ExamQuestion.query.filter_by( examquestionid = _examquestionid ).first()
        examquestion.choice = _choice 

    def deleteExamQuestion(_examid) :
        ExamQuestion.query.filter_by(examid = _examid).delete()

    def commitSession() :
        db.session.commit()    


'''
------------------------------------------------
    Section: REPORTEXAM
------------------------------------------------ 
''' 

class ReportExam(db.Model) :
    __tablename__ = 'reportexam'
    reportexamid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False)
    totalexam = db.Column(db.Integer, nullable=False)
    passedexam = db.Column(db.Integer, nullable=False)
    avgtime = db.Column(db.Integer)
    mintime = db.Column(db.Integer)
    maxtime = db.Column(db.Integer)

    def json(self):
        if self :
            return {
                    'reportexamid': self.reportexamid,
                    'userid': self.userid,
                    'totalexam': self.totalexam,
                    'passedexam': self.passedexam,
                    'avgtime': self.avgtime,
                    'mintime': self.mintime,
                    'maxtime': self.maxtime         
            }
        else :
            return None 
    
    def __repr__(self) :
        return json.dumps(
            {
                'reportexamid': self.reportexamid,
                'userid': self.userid,
                'totalexam': self.totalexam,
                'passedexam': self.passedexam,
                'avgtime': self.avgtime,
                'mintime': self.mintime,
                'maxtime': self.maxtime
            }
        )  

    def addExam(_userid, _haspassed, _time):
        reportexam = ReportExam.query.filter_by(userid = _userid).first()
        if reportexam :
            reportexam.totalexam = reportexam.totalexam + 1
            reportexam.passedexam = reportexam.passedexam + _haspassed
            reportexam.avgtime = (reportexam.avgtime + _time) /  2
            if reportexam.mintime > _time :
                reportexam.mintime = _time
            if reportexam.maxtime < _time :
                reportexam.maxtime = _time
        else :
            new_reportexam = ReportExam(userid=_userid, 
                                        totalexam=1,
                                        passedexam=_haspassed,
                                        avgtime=_time,
                                        mintime=_time,
                                        maxtime=_time)
            db.session.add(new_reportexam)

    def getReportExam(_userid) :
        return ReportExam.json(ReportExam.query.filter_by(userid = _userid).first())

    def commitSession() :
        db.session.commit()  

'''
------------------------------------------------
    Section: REPORTQUESTION
------------------------------------------------ 
''' 

class ReportQuestion(db.Model) :
    __tablename__ = 'reportquestion'
    reportquestionid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(20), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    totalattempt = db.Column(db.Integer, default=0)
    correctattempt = db.Column(db.Integer, default=0)

    def json(self):
        if self :
            return {
                    'reportquestionid': self.reportquestionid,
                    'userid': self.userid,
                    'subject': self.subject,
                    'difficulty': self.difficulty,
                    'totalattempt': self.totalattempt,
                    'correctattempt': self.correctattempt         
            }
        else :
            return None 
    
    def __repr__(self) :
        return json.dumps(
            {
                'reportquestionid': self.reportquestionid,
                'userid': self.userid,
                'subject': self.subject,
                'difficulty': self.difficulty,
                'totalattempt': self.totalattempt,
                'correctattempt': self.correctattempt
            }
        )  

    def addReportQuestion(_userid, _subject, _difficulty, _success):
        reportquestion = ReportQuestion.query.filter_by(userid=_userid,
                                                        subject=_subject,
                                                        difficulty=_difficulty).first()
        if reportquestion :
            reportquestion.totalattempt = reportquestion.totalattempt + 1
            reportquestion.correctattempt = reportquestion.correctattempt + _success
        else :
            new_reportquestion = ReportQuestion(userid=_userid,
                                                subject=_subject,
                                                difficulty=_difficulty,
                                                totalattempt=1,
                                                correctattempt=_success)            
            db.session.add(new_reportquestion)

    def getReportQuestion(_userid) :
        return [ ReportQuestion.json(report) for report in ReportQuestion.query.filter_by( userid = _userid ) ]

    def commitSession() :
        db.session.commit()
