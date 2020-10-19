from flask import Flask, jsonify, request, Response, current_app
from functools import wraps
from random import randint
import jwt
import datetime

from model import *
from . import main


'''
------------------------------------------------
    Section: LOGIN
------------------------------------------------ 
'''

@main.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = User.getUserByEmail(email)

    if user :
        if user['password'] == password :
            current_app.logger.info('Generating token for email '+str(email)+'.')
            token = jwt.encode(
                {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3000),
                    'id': user['userid']
                },
                current_app.config['SECRET_KEY'],
                algorithm = 'HS256'
            )
            return jsonify({'token': token.decode('utf-8') })
        else :
            current_app.logger.error('Cannot match user password for email '+str(email)+'.')
            return Response('', 401)
    else :
        current_app.logger.error('Cannot find email '+str(email)+'.')
        return Response('', 401)


def validate(f):
    @wraps(f)
    def wrappers(*args, **kwargs) :
        token = request.headers.get('token')
        try :
            jwt.decode(token, current_app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except :
            return Response('', 401)
    return wrappers


'''
------------------------------------------------
    Section: USER
------------------------------------------------ 
'''

@main.route('/user')
@validate
def get_user():
    token = request.headers.get('token')
    token_decoded = jwt.decode(
                                token, 
                                current_app.config['SECRET_KEY'], 
                                algorithm = 'HS256')
    userid = token_decoded['id']
    current_app.logger.info('Fetching user details for userid '+str(userid)+'.')
    user = User.getUserById(userid)
    isExamCountUpdate = 0
    if ExamCountTracker.getExamCountTrackerPerUser(user['userid']) :
        isExamCountUpdate = 1
    return {
        'name': user['name'],
        'email': user['email'],
        'password': user['password'],
        'examcount': user['examcount'],
        'userid': user['userid'],
        'isexamcountupdate': isExamCountUpdate
    }


@main.route('/updatepassword', methods = ['POST'])
@validate
def update_user_password():
    token = request.headers.get('token')
    token_decoded = jwt.decode(
                                token, 
                                current_app.config['SECRET_KEY'], 
                                algorithm = 'HS256')
    userid = token_decoded['id']
    data = request.get_json()
    password = data['password']
    current_app.logger.info('Updating password for userid '+str(userid)+' with value '+str(password)+'.')
    User.updatePasswordId(userid, password)
    User.commitSession()    
    user = User.getUserById(userid)
    current_app.logger.info(user)
    if user['password'] == password :
        return Response('', 200)
    else :
        return Response('', 500)


@main.route('/updateexamcount', methods = ['POST'])
@validate
def request_user_examcount():
    token = request.headers.get('token')
    token_decoded = jwt.decode(
                                token, 
                                current_app.config['SECRET_KEY'], 
                                algorithm = 'HS256')
    userid = token_decoded['id']
    data = request.get_json()
    examcount = data['examcount']
    current_app.logger.info('Checking if examcount update request already resepresent for user '+ str(userid) +'.')
    userrecord = ExamCountTracker.getExamCountTrackerPerUser(userid)
    if userrecord :
        current_app.logger.error('ExamCount update already present for user.')
        return Response('', 400)
    else :
        current_app.logger.info('Creating request for user.')
        ExamCountTracker.addExamCountTracker(userid, examcount)
        ExamCountTracker.commitSession()
        return Response('', 200)


@main.route('/applyexamcount/<int:userid>/<int:examcount>', methods = ['GET'])
@validate
def update_user_examcount(userid, examcount):
    token = request.headers.get('token')
    token_decoded = jwt.decode(
                                token, 
                                current_app.config['SECRET_KEY'], 
                                algorithm = 'HS256')
    myuserid = token_decoded['id']
    if myuserid != 0 :
        current_app.logger.error('Only an admin can update.')
        return Response('', 500)
    current_app.logger.info('Updating examcount for userid '+str(userid)+' with value '+str(examcount)+'.')
    user = User.getUserById(userid)
    current_app.logger.info(user)
    User.updateExamCountById(userid, examcount)
    User.commitSession()
    updateduser = User.getUserById(userid)
    current_app.logger.info(updateduser)
    if updateduser['examcount'] == (user['examcount'] + examcount) :
        ExamCountTracker.deleteExamCountTracker(userid)
        ExamCountTracker.commitSession()
        return Response('', 200)
    else :
        return Response('', 500)


@main.route('/createuser', methods = ['POST'])
def create_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    current_app.logger.info('Creating user with '+ str(name) +', email '+ str(email) +'.')
    doexist = User.getUserByEmail(email)
    if doexist :
        current_app.logger.error('User already exist, email should be unique.')
        return Response('', 500)
    else :
        current_app.logger.info('No existing user has same email thus proceeding to create.')
        User.addUser(name, email, password)
        User.commitSession()
        doexist = User.getUserByEmail(email)
        if doexist :
            current_app.logger.info('User created successfully.')
            return Response('', 200)
        else :
            current_app.logger.error('Unkown error occured while creating user.')
            return Response('', 500)


'''
------------------------------------------------
    Section: EXAM
------------------------------------------------ 
'''

@main.route('/createexam', methods = ['GET'])
@validate
def create_exam():
    token = request.headers.get('token')
    token_decoded = jwt.decode(
                                token, 
                                current_app.config['SECRET_KEY'], 
                                algorithm = 'HS256')
    userid = token_decoded['id']
    allowed_exam = User.getUserById(userid)['examcount']
    current_app.logger.debug('User '+ str(userid) +' has '+ str(allowed_exam) +' exams available.')
    if allowed_exam < 1 :
        current_app.logger.info('User '+ str(userid) +' has no available exams.')
        return Response('', 403)
    current_exam = Exam.getActiveExamForUser(userid)
    if not current_exam :
        current_app.logger.info('Creating Exam for User '+str(userid)+'.')
        Exam.addExam(userid)
        current_exam = Exam.getActiveExamForUser(userid)
        if not current_exam :
            current_app.logger.error('Cannot create Exam for User '+ str(userid) +'.')
            return Response('', 500)
        else :
            current_app.logger.info('Creating questions for User '+str(userid)+' and Exam '+ str(current_exam) +'.')
            #for s in ['history','geography','mathemetics','science','gk','aptitude'] :
            for s in current_app.config['EXAM_SUBJECT_LIST'] :
                for l in ['simple', 'difficult'] :
                    current_app.logger.info('Adding questions for subject '+ str(s) +' and difficulty level '+ str(l) +'.')
                    available_questions = Question.getQuestionByCategory(s, l)
                    list_length = len(available_questions)
                    if l == 'simple' :
                        total_question = current_app.config['EXAM_MAX_SIMPLE_QUESTION_PER_SUBJECT']
                    else :
                        total_question = current_app.config['EXAM_MAX_DIFFICULT_QUESTION_PER_SUBJECT']
                    for i in range(total_question) :
                        question_index = randint(0, list_length-1)
                        question_id = available_questions[question_index]
                        current_app.logger.info('Adding question with id '+ str(question_id) +'.')
                        ExamQuestion.addExamQuestion(current_exam, question_id)
            ExamQuestion.commitSession()
            Exam.commitSession()
            User.updateExamCountById(userid, allowed_exam - 1)
            User.commitSession()
            return Response('', 200)
    else :
        current_app.logger.error('Already active Exam '+ str(current_exam) +' ongoing for  User '+ str(userid) +'.')
        return Response('', 400)


@main.route('/userexam', methods = ['GET'])
@validate
def user_exam():
    token = request.headers.get('token')
    token_decoded = jwt.decode( token, 
                                current_app.config['SECRET_KEY'], 
                                algorithm = 'HS256')
    userid = token_decoded['id']
    current_exam = Exam.getActiveExamForUser(userid)
    if current_exam :
        current_app.logger.info('Checking if user completed it exam time.')
        _exam_ongoing = Exam.getExamById(current_exam)
        _start_time = _exam_ongoing['starttime']
        _time = datetime.datetime.now()
        max_exam_time = current_app.config['EXAM_MAX_TIME_MINUTES']
        _end_time = _start_time + datetime.timedelta(minutes=max_exam_time)
        if _end_time < _time :
            current_app.logger.info('User already spend more time than allocated, ending exam.')
            Exam.endExam(current_exam)
            Exam.commitSession()
            current_exam = None
    if current_exam :
        current_app.logger.info('Exam ongoing for User '+str(userid)+'.')
        question_list = ExamQuestion.getUnansweredExamQuestion(current_exam)
        current_app.logger.debug('List of questions to answer.')
        current_app.logger.debug(question_list)
        if len(question_list) == 0 :
            current_app.logger.info('Exam '+ str(current_exam) +' completed for User '+str(userid)+'.')
            Exam.endExam(current_exam)
            Exam.commitSession()
            result = {}
        else :
            current_app.logger.info('Fetching next question for Exam '+ str(current_exam) +' and User '+str(userid)+'.')
            question_list.sort(key=lambda q: q['examquestionid'])
            next_question = question_list[0]['questionid']
            current_app.logger.debug('Question selected: ')
            current_app.logger.debug(next_question)
            result = Question.getQuestionById(next_question)
            current_app.logger.debug('Return Value:')
            current_app.logger.debug(result)
    else :
        current_app.logger.info('No Exam ongoing for User '+str(userid)+' will generate exam result.')
        completed_exam = Exam.getCompletedExamForUser(userid)
        completed_exam.sort(reverse=True)
        current_app.logger.debug('Completed exams : ')
        current_app.logger.debug(completed_exam)
        if len(completed_exam) > 0 :
            result_exam = completed_exam[0]
            pass_percentage = current_app.config['EXAM_PASS_PERCENTAGE']
            question_list = ExamQuestion.getExamQuestion(result_exam)
            current_app.logger.debug('List of questions : ')
            current_app.logger.debug(question_list)        
            total_question = 0
            total_success = 0
            for question in question_list :
                current_app.logger.debug('Questions Considered: ')
                current_app.logger.debug(question) 
                total_question += 1
                correct_answer = Question.getQuestionById(question['questionid'])['answer']
                current_app.logger.debug('Questions Correct Answer: '+ str(correct_answer) +'.')
                if correct_answer == question['choice'] :
                    total_success += 1
            total_percentage = (total_success / total_question) * 100
            current_app.logger.debug('Percentage: '+ str(total_percentage) +'.')
            if total_percentage > pass_percentage :
                exam_status = "PASS"
            else :
                exam_status = "FAILED"
            current_app.logger.debug('Exam Status: '+ str(exam_status) +'.')
            result = {
                'result': {
                    'status': exam_status,
                    'percentage': total_percentage,
                    'start': str(Exam.getExamById(result_exam)['starttime']),
                    'end': str(Exam.getExamById(result_exam)['endtime'])
                }
            }
            current_app.logger.debug('Return Value:')
            current_app.logger.debug(result)
        else :
            current_app.logger.info('No Exam ongoing for User '+str(userid)+' also no history of Exam.')
            result = {}
    return result


@main.route('/submitanswer', methods = ['POST'])
@validate
def submit_answer():
    token = request.headers.get('token')
    token_decoded = jwt.decode( token, 
                                current_app.config['SECRET_KEY'], 
                                algorithm = 'HS256')
    userid = token_decoded['id']
    data = request.get_json()
    choice = data['choice']    
    current_exam = Exam.getActiveExamForUser(userid)
    if current_exam :
        current_app.logger.info('Exam '+ str(current_exam) +' is ongoing for User '+str(userid)+'.')
        question_list = ExamQuestion.getUnansweredExamQuestion(current_exam)
        current_app.logger.debug('List of questions to answer.')
        current_app.logger.debug(question_list)
        question_list.sort(key=lambda q: q['examquestionid'])
        next_question = question_list[0]['examquestionid']
        current_app.logger.info('Answer will be registered for Question '+ str(next_question) +'.')
        ExamQuestion.setAnswerToQuestion(next_question, choice)
        ExamQuestion.commitSession()
        if len(question_list) == 1 :
            current_app.logger.info('Since Question'+ str(next_question) +' was the last question in exam thus ending exam.')
            Exam.endExam(current_exam)
            Exam.commitSession()
        return Response('', 200)
    else :
        current_app.logger.error('No such Active Exam '+ str(current_exam) +' ongoing for  User '+ str(userid) +'.')
        return Response('', 400)

'''
------------------------------------------------
    Section: REPORT
------------------------------------------------ 
'''
@main.route('/getreport', methods = ['GET'])
@validate
def create_report():
    token = request.headers.get('token')
    token_decoded = jwt.decode( token, 
                                current_app.config['SECRET_KEY'], 
                                algorithm = 'HS256')
    userid = token_decoded['id']
    completed_exam = Exam.getCompletedExamForUser(userid)
    if len(completed_exam) > 0 :
        current_app.logger.debug('Starting to gererate latest exam result.')
        completed_exam.sort(reverse=True)
        result_exam = completed_exam[0]
        current_app.logger.info('Latest exam: '+ str(result_exam))
        pass_percentage = current_app.config['EXAM_PASS_PERCENTAGE']
        question_list = ExamQuestion.getExamQuestion(result_exam)
        current_app.logger.debug('Question List: ')
        current_app.logger.debug(question_list)
        total_question = 0
        total_success = 0
        aggregate_catagory = {}
        for question in question_list :
            current_app.logger.debug('Question Analysed: ')
            current_app.logger.debug(question)            
            question_detail = Question.getQuestionById(question['questionid'])
            current_app.logger.debug('Question Details: ')
            current_app.logger.debug(question_detail)
            correct_answer = question_detail['answer']
            total_question += 1
            if correct_answer == question['choice'] :
                total_success += 1
            if question_detail['subject'] in aggregate_catagory.keys() :
                _subject = aggregate_catagory[question_detail['subject']]
                current_app.logger.debug('Subject Record Present: ')
                current_app.logger.debug(_subject)                
                if question_detail['difficulty'] in _subject :
                    _difficulty = _subject[question_detail['difficulty']]
                    current_app.logger.debug('Difficulty Record Present: ')
                    current_app.logger.debug(_difficulty)
                    _difficulty['total'] += 1
                    if correct_answer == question['choice'] :
                        _difficulty['correct'] += 1
                else :
                    current_app.logger.debug('Difficulty Record not present thus creating.')
                    _difficulty = {}
                    _difficulty['total'] = 1
                    if correct_answer == question['choice'] :
                        _difficulty['correct'] = 1
                    else :
                        _difficulty['correct'] = 0
                    current_app.logger.debug('Difficulty Record: ')
                    current_app.logger.debug(_difficulty)
                    _subject[question_detail['difficulty']] = _difficulty
            else :
                current_app.logger.debug('Subject Record not present thus creating.')
                _subject = {}
                _difficulty = {}
                _difficulty['total'] = 1
                if correct_answer == question['choice'] :
                    _difficulty['correct'] = 1
                else :
                    _difficulty['correct'] = 0
                current_app.logger.debug('Difficulty Record: ')
                current_app.logger.debug(_difficulty)
                _subject[question_detail['difficulty']] = _difficulty
                aggregate_catagory[question_detail['subject']] = _subject
            current_app.logger.debug('Current Agreegated Result: ')
            current_app.logger.debug(aggregate_catagory)
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
    current_app.logger.debug('Result retruned: ')
    current_app.logger.debug(result)
    return result


'''
------------------------------------------------
    Section: Query
------------------------------------------------ 
'''

@main.route('/query', methods = ['POST'])
def add_query():
    data = request.get_json()
    email = data['email']
    query = data['query']
    if QueryReport.getQueryByEmail(email) :
        return Response('', 500)
    else :        
        QueryReport.addQuery(email, query)
        QueryReport.commitSession()
        return Response('', 200)