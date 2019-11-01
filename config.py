
class Config(object) :
  """
    Common configuration
  """
#

class DevelopmentConfig(Config) :
  """
    Development configuration
  """
  DEBUG = True
  SQLALCHEMY_ECHO = True
  SECRET_KEY = 'p9Bv<3Eid9%$i01'
  SQLALCHEMY_DATABASE_URI = ''
#

class ProductionConfig(Config) :
  """
    Production configuration
  """
  DEBUG = False
  SERVER_NAME="127.0.0.1:8080"
#

application_configuration = {
  "development" : DevelopmentConfig,
  "production" : ProductionConfig
}

