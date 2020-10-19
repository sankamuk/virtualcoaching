import os

TESTING = True
DEBUG = False
SQLALCHEMY_ECHO = False
SECRET_KEY = 'sankar'
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir, '../app_test.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
CORS_HEADERS = 'Content-Type'
WTF_CSRF_ENABLED = False
EXAM_SUBJECT_LIST = ['test']
EXAM_MAX_SIMPLE_QUESTION_PER_SUBJECT = 1
EXAM_MAX_DIFFICULT_QUESTION_PER_SUBJECT = 1
EXAM_PASS_PERCENTAGE = 40
EXAM_MAX_TIME_MINUTES = 5