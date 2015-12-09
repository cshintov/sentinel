#Import flask and template operators
from flask import Flask, render_template

# Import MongoEngine
from flask.ext.mongoengine import MongoEngine

# Define the WSGI application object
app = Flask(__name__)

# Configurations
#app.config["MONGODB_SETTINGS"] = {'DB': "sentinel"}
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
