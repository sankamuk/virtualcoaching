import os

DEBUG = True
SQLALCHEMY_ECHO = True
SECRET_KEY = '__PASSWORD__'
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir, '../app_dev.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
CORS_HEADERS = 'Content-Type'
EXAM_SUBJECT_LIST = ['history','geography','mathemetics','science','gk','aptitude']
EXAM_MAX_SIMPLE_QUESTION_PER_SUBJECT = 1
EXAM_MAX_DIFFICULT_QUESTION_PER_SUBJECT = 1
EXAM_PASS_PERCENTAGE = 40
EXAM_MAX_TIME_MINUTES = 5
