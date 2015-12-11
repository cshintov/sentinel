#Import flask and template operators
from flask import Flask, render_template

# Import MongoEngine
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from sentinel.utils.session import MongoSessionInterface

# Define the WSGI application object
app = Flask(__name__)

app.session_interface = MongoSessionInterface(db='sentinel_app')

#flask-login setup
login_manager = LoginManager()
login_manager.init_app(app)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = MongoEngine(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route("/<name>")
def hello(name):
    return "hello {}".format(name)

# Register blueprint(s)
def register_blueprints(app):
	""" to prevent circular imports """
	from sentinel.auth.controllers import auth
	from sentinel.home.controllers import home
	app.register_blueprint(auth)
	app.register_blueprint(home)

register_blueprints(app)
