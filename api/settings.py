from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sankar'
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['EXAM_MAX_SIMPLE_QUESTION_PER_SUBJECT'] = 1
app.config['EXAM_MAX_DIFFICULT_QUESTION_PER_SUBJECT'] = 1
app.config['EXAM_PASS_PERCENTAGE'] = 40
app.config['EXAM_MAX_TIME_MINUTES'] = 5
cors = CORS(app, resources={r"/*": {"origins": "*"}})
