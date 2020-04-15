# Views are handlers that responds to requests from browsers and clients
# Handlers are written as Python Functions. 
# Each View Function is mapped to one or more request URLs.

from app import app

# Function to render the templates
from flask import render_template

# Map 2 Routes to the same Function. Can map a single route too.

@app.route('/')
@app.route('/index')
def index():
	return "Welcome to AcadOverflow!"

@app.route('/login/<name>')
def hello_name(name):
	return "Hello, %s!" % name

@app.route('/question/<int:questionID>')
def show_blog(questionID):
	return "Question Number: %d" % questionID

# Simple returns a string to the client :-)
 