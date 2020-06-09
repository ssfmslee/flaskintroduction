from flask import Flask, g, render_template, session
# from flask.ext.sqlalchemy import SQLAlchemy 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('snowfort.config')

# the following command is added by Chen
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

# Import Blueprints
from blueprints import app_blueprints

for blueprint in app_blueprints:
  app.register_blueprint(blueprint)

# Main Application Routes
from blueprints.users.models import User

@app.before_request
def before_request():
  """
  Set up before all requests.
  """
  g.user = None
  if 'user_id' in session:
    g.user = User.query.get(session['user_id'])

@app.route('/')
def index():
  """
  Index Welcome Page
  """
  return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
  """
  404 File Not Found
  """
  return render_template('404.html'), 404

@app.route('/jquery')
def testjquery():
  """
  Index Welcome Page
  """
  return render_template('testjquery.html')