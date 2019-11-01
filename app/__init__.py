# Third party
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy

# Internal 
from config import application_configuration

# Initialization
db = SQLAlchemy()

# Application Context Initialization
def application(config_name) :
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_object(application_configuration[config_name])
  app.config.from_pyfile("config.py")
  db.init_app(app)

  from .home import home as home_blueprint
  app.register_blueprint(home_blueprint)

  @app.route('/')
  def index() :
    return redirect('/home')

  return app

