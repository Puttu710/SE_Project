# Views are handlers that responds to requests from browsers and clients
# Handlers are written as Python Functions. 
# Each View Function is mapped to one or more request URLs.

from app import app

# Function to render the templates
from flask import render_template

# Import to use redirect and url_for methods
from flask import url_for, redirect

# Map 2 Routes to the same Function. Can map a single route too.

@app.route('/')
@app.route('/index')
def index():
	user = {'name': 'guest'}
	posts = [
		{
			'author': {'name': 'user1'},
			'question': 'The question 1 in detail.' 
		},
		{
			'author': {'name': 'user2'},
			'question': 'The question 2 in detail.' 
		}
	]
	return render_template('index.html',title='Home',user=user,posts=posts)

@app.route('/login/<name>')
def hello_name(name):
	return "Hello, %s!" % name

@app.route('/question/<int:questionID>')
def show_blog(questionID):
	return "Question Number: %d" % questionID

# Simple returns a string to the client 