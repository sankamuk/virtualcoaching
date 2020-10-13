from flask import Flask, jsonify, request, Response
from functools import wraps
from random import randint
from settings import *
from Model import *
import jwt
import datetime


'''
------------------------------------------------
    Section: LOGIN
------------------------------------------------ 
'''

@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = User.getUserByEmail(email)

    if user :
        if user['password'] == password :
            app.logger.info('Generating token for email '+str(email)+'.')
            token = jwt.encode(
                {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3000),
                    'id': user['userid']
                },
                app.config['SECRET_KEY'],
                algorithm = 'HS256'
            )
            return jsonify({'token': token.decode('utf-8') })
        else :
            app.logger.error('Cannot match user password for email '+str(email)+'.')
            return Response('', 401)
    else :
        app.logger.error('Cannot find email '+str(email)+'.')
        return Response('', 401)

def validate(f):
    @wraps(f)
    def wrappers(*args, **kwargs) :
        token = request.headers.get('token')
        try :
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except :
            return Response('', 401)
    return wrappers


'''
------------------------------------------------
    Section: USER
------------------------------------------------ 
'''

@app.route('/user')
@validate
def get_user():
    token = request.headers.get('token')
    token_decoded = jwt.decode(
                                token, 
                                app.config['SECRET_KEY'], 
                                algorithm = 'HS256')
    userid = token_decoded['id']
    app.logger.info('Fetching user details for userid '+str(userid)+'.')
    return User.getUserById(userid)

@app.route('/updatepassword', methods = ['POST'])
@validate
def update_user_password():
    token = request.headers.get('token')
    token_decoded = jwt.decode(
                                token, 
                                app.config['SECRET_KEY'], 
                                algorithm = 'HS256')
    userid = token_decoded['id']
    data = request.get_json()
    password = data['password']
    app.logger.info('Updating password for userid '+str(userid)+' with value '+str(password)+'.')
    User.updatePasswordId(userid, password)
    User.commitSession()    
    user = User.getUserById(userid)
    app.logger.info(user)
    if user['password'] == password :
        return Response('', 200)
    else :
        return Response('', 500)


@app.route('/updateexamcount', methods = ['POST'])
@validate
def update_user_examcount():
    token = request.headers.get('token')
    token_decoded = jwt.decode(
                                token, 
                                app.config['SECRET_KEY'], 
                                algorithm = 'HS256')
    userid = token_decoded['id']
    data = request.get_json()
    examcount = data['examcount']
    app.logger.info('Updating examcount for userid '+str(userid)+' with value '+str(examcount)+'.')
    User.updateExamCountById(userid, examcount)
    User.commitSession()    
    user = User.getUserById(userid)
    app.logger.info(user)
    if user['examcount'] == examcount :
        return Response('', 200)
    else :
        return Response('', 500)


'''
------------------------------------------------
    Section: EXAM
------------------------------------------------ 
'''

@app.route('/createexam', methods = ['GET'])
@validate
def create_exam():
    token = request.headers.get('token')
    token_decoded = jwt.decode(
                                token, 
                                app.config['SECRET_KEY'], 
                                algorithm = 'HS256')
    userid = token_decoded['id']
    allowed_exam = User.getUserById(userid)['examcount']
    app.logger.debug('User '+ str(userid) +' has '+ str(allowed_exam) +' exams available.')
    if allowed_exam < 1 :
        app.logger.info('User '+ str(userid) +' has no available exams.')
        return Response('', 403)
    current_exam = Exam.getActiveExamForUser(userid)
    if not current_exam :
        app.logger.info('Creating Exam for User '+str(userid)+'.')
        Exam.addExam(userid)
        current_exam = Exam.getActiveExamForUser(userid)
        if not current_exam :
            app.logger.error('Cannot create Exam for User '+ str(userid) +'.')
            return Response('', 500)
        else :
            app.logger.info('Creating questions for User '+str(userid)+' and Exam '+ str(current_exam) +'.')
            for s in ['history','geography','mathemetics','science','gk','aptitude'] :
                for l in ['simple', 'difficult'] :
                    app.logger.info('Adding questions for subject '+ str(s) +' and difficulty level '+ str(l) +'.')
                    available_questions = Question.getQuestionByCategory(s, l)
                    list_length = len(available_questions)
                    if l == 'simple' :
                        total_question = app.config['EXAM_MAX_SIMPLE_QUESTION_PER_SUBJECT']
                    else :
                        total_question = app.config['EXAM_MAX_DIFFICULT_QUESTION_PER_SUBJECT']
                    for i in range(total_question) :
                        question_index = randint(0, list_length-1)
                        question_id = available_questions[question_index]
                        app.logger.info('Adding question with id '+ str(question_id) +'.')
                        ExamQuestion.addExamQuestion(current_exam, question_id)
            ExamQuestion.commitSession()
            Exam.commitSession()
            User.updateExamCountById(userid, allowed_exam - 1)
            User.commitSession()
            return Response('', 200)
    else :
        app.logger.error('Already active Exam '+ str(current_exam) +' ongoing for  User '+ str(userid) +'.')
        return Response('', 400)

@app.route('/userexam', methods = ['GET'])
@validate
def user_exam():
    token = request.headers.get('token')
    token_decoded = jwt.decode( token, 
                                app.config['SECRET_KEY'], 
                                algorithm = 'HS256')
    userid = token_decoded['id']
    current_exam = Exam.getActiveExamForUser(userid)
    if current_exam :
        app.logger.info('Checking if user completed it exam time.')
        _exam_ongoing = Exam.getExamById(current_exam)
        _start_time = _exam_ongoing['starttime']
        _time = datetime.datetime.now()
        max_exam_time = app.config['EXAM_MAX_TIME_MINUTES']
        _end_time = _start_time + datetime.timedelta(minutes=max_exam_time)
        if _end_time < _time :
            app.logger.info('User already spend more time than allocated, ending exam.')
            Exam.endExam(current_exam)
            Exam.commitSession()
            current_exam = None
    if current_exam :
        app.logger.info('Exam ongoing for User '+str(userid)+'.')
        question_list = ExamQuestion.getUnansweredExamQuestion(current_exam)
        app.logger.debug('List of questions to answer.')
        app.logger.debug(question_list)
        if len(question_list) == 0 :
            app.logger.info('Exam '+ str(current_exam) +' completed for User '+str(userid)+'.')
            Exam.endExam(current_exam)
            Exam.commitSession()
            result = {}
        else :
            app.logger.info('Fetching next question for Exam '+ str(current_exam) +' and User '+str(userid)+'.')
            question_list.sort(key=lambda q: q['examquestionid'])
            next_question = question_list[0]['questionid']
            app.logger.debug('Question selected: ')
            app.logger.debug(next_question)
            result = Question.getQuestionById(next_question)
            app.logger.debug('Return Value:')
            app.logger.debug(result)
    else :
        app.logger.info('No Exam ongoing for User '+str(userid)+' will generate exam result.')
        completed_exam = Exam.getCompletedExamForUser(userid)
        completed_exam.sort(reverse=True)
        app.logger.debug('Completed exams : ')
        app.logger.debug(completed_exam)
        if len(completed_exam) > 0 :
            result_exam = completed_exam[0]
            pass_percentage = app.config['EXAM_PASS_PERCENTAGE']
            question_list = ExamQuestion.getExamQuestion(result_exam)
            app.logger.debug('List of questions : ')
            app.logger.debug(question_list)        
            total_question = 0
            total_success = 0
            for question in question_list :
                app.logger.debug('Questions Considered: ')
                app.logger.debug(question) 
                total_question += 1
                correct_answer = Question.getQuestionById(question['questionid'])['answer']
                app.logger.debug('Questions Correct Answer: '+ str(correct_answer) +'.')
                if correct_answer == question['choice'] :
                    total_success += 1
            total_percentage = (total_success / total_question) * 100
            app.logger.debug('Percentage: '+ str(total_percentage) +'.')
            if total_percentage > pass_percentage :
                exam_status = "PASS"
            else :
                exam_status = "FAILED"
            app.logger.debug('Exam Status: '+ str(exam_status) +'.')
            result = {
                'result': {
                    'status': exam_status,
                    'percentage': total_percentage,
                    'start': str(Exam.getExamById(result_exam)['starttime']),
                    'end': str(Exam.getExamById(result_exam)['endtime'])
                }
            }
            app.logger.debug('Return Value:')
            app.logger.debug(result)
        else :
            app.logger.info('No Exam ongoing for User '+str(userid)+' also no history of Exam.')
            result = {}
    return result

@app.route('/submitanswer', methods = ['POST'])
@validate
def submit_answer():
    token = request.headers.get('token')
    token_decoded = jwt.decode( token, 
                                app.config['SECRET_KEY'], 
                                algorithm = 'HS256')
    userid = token_decoded['id']
    data = request.get_json()
    choice = data['choice']    
    current_exam = Exam.getActiveExamForUser(userid)
    if current_exam :
        app.logger.info('Exam '+ str(current_exam) +' is ongoing for User '+str(userid)+'.')
        question_list = ExamQuestion.getUnansweredExamQuestion(current_exam)
        app.logger.debug('List of questions to answer.')
        app.logger.debug(question_list)
        question_list.sort(key=lambda q: q['examquestionid'])
        next_question = question_list[0]['examquestionid']
        app.logger.info('Answer will be registered for Question '+ str(next_question) +'.')
        ExamQuestion.setAnswerToQuestion(next_question, choice)
        ExamQuestion.commitSession()
        if len(question_list) == 1 :
            app.logger.info('Since Question'+ str(next_question) +' was the last question in exam thus ending exam.')
            Exam.endExam(current_exam)
            Exam.commitSession()
        return Response('', 200)
    else :
        app.logger.error('No such Active Exam '+ str(current_exam) +' ongoing for  User '+ str(userid) +'.')
        return Response('', 400)

'''
------------------------------------------------
    Section: REPORT
------------------------------------------------ 
'''
@app.route('/getreport', methods = ['GET'])
@validate
def create_report():
    token = request.headers.get('token')
    token_decoded = jwt.decode( token, 
                                app.config['SECRET_KEY'], 
                                algorithm = 'HS256')
    userid = token_decoded['id']
    completed_exam = Exam.getCompletedExamForUser(userid)
    if len(completed_exam) > 0 :
        app.logger.debug('Starting to gererate latest exam result.')
        completed_exam.sort(reverse=True)
        result_exam = completed_exam[0]
        app.logger.info('Latest exam: '+ str(result_exam))
        pass_percentage = app.config['EXAM_PASS_PERCENTAGE']
        question_list = ExamQuestion.getExamQuestion(result_exam)
        app.logger.debug('Question List: ')
        app.logger.debug(question_list)
        total_question = 0
        total_success = 0
        aggregate_catagory = {}
        for question in question_list :
            app.logger.debug('Question Analysed: ')
            app.logger.debug(question)            
            question_detail = Question.getQuestionById(question['questionid'])
            app.logger.debug('Question Details: ')
            app.logger.debug(question_detail)
            correct_answer = question_detail['answer']
            total_question += 1
            if correct_answer == question['choice'] :
                total_success += 1
            if question_detail['subject'] in aggregate_catagory.keys() :
                _subject = aggregate_catagory[question_detail['subject']]
                app.logger.debug('Subject Record Present: ')
                app.logger.debug(_subject)                
                if question_detail['difficulty'] in _subject :
                    _difficulty = _subject[question_detail['difficulty']]
                    app.logger.debug('Difficulty Record Present: ')
                    app.logger.debug(_difficulty)
                    _difficulty['total'] += 1
                    if correct_answer == question['choice'] :
                        _difficulty['correct'] += 1
                else :
                    app.logger.debug('Difficulty Record not present thus creating.')
                    _difficulty = {}
                    _difficulty['total'] = 1
                    if correct_answer == question['choice'] :
                        _difficulty['correct'] = 1
                    else :
                        _difficulty['correct'] = 0
                    app.logger.debug('Difficulty Record: ')
                    app.logger.debug(_difficulty)
                    _subject[question_detail['difficulty']] = _difficulty
            else :
                app.logger.debug('Subject Record not present thus creating.')
                _subject = {}
                _difficulty = {}
                _difficulty['total'] = 1
                if correct_answer == question['choice'] :
                    _difficulty['correct'] = 1
                else :
                    _difficulty['correct'] = 0
                app.logger.debug('Difficulty Record: ')
                app.logger.debug(_difficulty)
                _subject[question_detail['difficulty']] = _difficulty
                aggregate_catagory[question_detail['subject']] = _subject
            app.logger.debug('Current Agreegated Result: ')
            app.logger.debug(aggregate_catagory)
        total_percentage = (total_success / total_question) * 100
        if total_percentage > pass_percentage :
            exam_status = "PASS"
        else :
            exam_status = "FAILED"
        latest_result = {
            'status': exam_status,
            'percentage': total_percentage,
            'start': Exam.getExamById(result_exam)['starttime'],
            'end': Exam.getExamById(result_exam)['endtime'],
            'aggregate': aggregate_catagory
        }
    else :
        latest_result = None
    result = {}
    if latest_result :
        result['latest'] = latest_result
    exam_result = ReportExam.getReportExam(userid)
    if exam_result :
        result['exam'] = exam_result
    question_result = ReportQuestion.getReportQuestion(userid)
    if len(question_result) > 0 :
        result['question'] = question_result
    app.logger.debug('Result retruned: ')
    app.logger.debug(result)
    return result


if __name__ == '__main__':
    app.run(port=8080, debug=True)


