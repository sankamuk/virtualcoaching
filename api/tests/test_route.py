import json
import unittest
from app import application, db
from model import *

class RouteTestCase(unittest.TestCase):

    token = None

    def setUp(self):
        self.app = application('testing')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        self.client = self.app.test_client()
        db.create_all()
        User.addUser('test', 'test@test.com', 'test')
        User.updateExamCountById(1, 5)
        User.commitSession()
        Question.addQuestion('test', 'difficult', 't-d-q-1', 't-d-o-1-1', 't-d-o-2-1', 't-d-o-3-1', 't-d-o-4-1', 1)  
        Question.addQuestion('test', 'simple', 't-s-q-1', 't-s-o-1-1', 't-s-o-2-1', 't-s-o-3-1', 't-s-o-4-1', 2)
        Question.commitSession()

    def tearDown(self):
        db.drop_all()
        self.app_ctx.pop()

    def test_login_functions(self):    
        r = self.client.post('/login', data=json.dumps({'email': 'test@test.com', 'password': 'test'}), content_type='application/json')
        self.assertEqual(r.status_code, 200)

    def test_user_functions(self): 
        r1 = self.client.post('/login', data=json.dumps({'email': 'test@test.com', 'password': 'test'}), content_type='application/json')
        t = json.loads(r1.get_data(as_text=True))['token']
        r2 = self.client.get('/user', headers={ 'token': t })
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(json.loads(r2.get_data(as_text=True))['name'], 'test')

    def test_examcount_functions(self):        
        r1 = self.client.post('/login', data=json.dumps({'email': 'test@test.com', 'password': 'test'}), content_type='application/json')
        t = json.loads(r1.get_data(as_text=True))['token']
        r2 = self.client.post('/updateexamcount', data=json.dumps({'examcount': 5}), content_type='application/json', headers={ 'token': t })
        self.assertEqual(r2.status_code, 200)
        r3 = self.client.get('/applyexamcount/1/5', headers={ 'token': t })
        self.assertEqual(r3.status_code, 500)

    def test_exam_functions(self): 
        r1 = self.client.post('/login', data=json.dumps({'email': 'test@test.com', 'password': 'test'}), content_type='application/json')
        t = json.loads(r1.get_data(as_text=True))['token']
        r2 = self.client.get('/createexam', headers={ 'token': t })        
        self.assertEqual(r2.status_code, 200)
        r3 = self.client.get('/userexam', headers={ 'token': t }) 
        self.assertEqual(r3.status_code, 200)
        self.assertTrue(json.loads(r3.get_data(as_text=True))['question'])
        r4 = self.client.post('/submitanswer', data=json.dumps({'choice': 1}), content_type='application/json', headers={ 'token': t })
        self.assertEqual(r4.status_code, 200)
        r5 = self.client.get('/userexam', headers={ 'token': t }) 
        self.assertEqual(r5.status_code, 200)
        self.assertTrue(json.loads(r5.get_data(as_text=True))['question'])    
        r6 = self.client.post('/submitanswer', data=json.dumps({'choice': 2}), content_type='application/json', headers={ 'token': t })
        self.assertEqual(r6.status_code, 200)
        r5 = self.client.get('/userexam', headers={ 'token': t }) 
        self.assertEqual(r5.status_code, 200)
        self.assertTrue(json.loads(r5.get_data(as_text=True))['result'])        

