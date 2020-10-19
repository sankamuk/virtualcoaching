import unittest
from app import application, db
from model import *

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = application('testing')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.app_ctx.pop()


    def test_user_functions(self):
        User.addUser('test', 'test@test.com', 'test')
        User.commitSession()
        u = User.getUserById(1) 
        self.assertEqual(len(User.getAllUser()),1)
        self.assertEqual(u['name'], 'test')
        User.updatePasswordId(1, 'sankar') 
        User.commitSession()
        u = User.getUserById(1)
        self.assertEqual(u['password'], 'sankar')

    def test_query_functions(self):
        QueryReport.addQuery('test@test.com', 'test')
        QueryReport.commitSession()
        q = QueryReport.getQueryByEmail('test@test.com')
        self.assertEqual(q['querytext'], 'test')

    def test_examcount_functions(self):
        ExamCountTracker.addExamCountTracker(1,1)
        ExamCountTracker.commitSession()
        self.assertEqual(len(ExamCountTracker.getExamCountTrackerNotNotified()), 1)
        ExamCountTracker.updateExamCountTrackerAlreadyNotified(1)
        ExamCountTracker.commitSession()
        self.assertEqual(len(ExamCountTracker.getExamCountTrackerNotNotified()), 0)


    def test_question_functions(self):
        Question.addQuestion('test', 'difficult', 't-d-q-1', 't-d-o-1-1', 't-d-o-2-1', 't-d-o-3-1', 't-d-o-4-1', 1)  
        Question.addQuestion('test', 'simple', 't-s-q-1', 't-s-o-1-1', 't-s-o-2-1', 't-s-o-3-1', 't-s-o-4-1', 2)
        Question.commitSession()
        q = Question.getQuestionById(1)
        self.assertEqual(q['question'], 't-d-q-1')
        self.assertEqual(len(Question.getQuestionByCategory('test', 'difficult')), 1)

    def test_exam_functions(self):
        Exam.addExam(1)
        Exam.commitSession()
        self.assertEqual(Exam.getActiveExamForUser(1), 1)
        self.assertEqual(len(Exam.getCompletedExamForUser(1)), 0)

    def test_examquestion_functions(self):
        ExamQuestion.addExamQuestion(1, 1)
        ExamQuestion.addExamQuestion(1, 2)
        ExamQuestion.commitSession()
        self.assertEqual(len(ExamQuestion.getUnansweredExamQuestion(1)), 2)
        ExamQuestion.setAnswerToQuestion(1, 1)
        ExamQuestion.commitSession()
        self.assertEqual(len(ExamQuestion.getUnansweredExamQuestion(1)), 1)







 

