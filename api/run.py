import os
from app import application, db

if __name__ == "__main__" :
  config_name = os.getenv("FLASK_CONFIG")
  app = application(config_name)
  with app.app_context():
  	db.create_all()
  app.run()