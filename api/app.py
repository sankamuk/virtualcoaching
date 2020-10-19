# Third party
import os
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def application(config_name) :
  app = Flask(__name__)
  cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
  app.config.from_pyfile(cfg)
  cors = CORS(app, resources={r"/*": {"origins": "*"}})
  db.init_app(app)

  from main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  return app