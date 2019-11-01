from . import home

@home.route('/home')
def home() :
  return "At Home!!!"
