import os
from app import application

config_name = os.getenv("FLASK_CONFIG")
app = application(config_name)

if __name__ == "__main__" :
  app.run()
