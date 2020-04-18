# Views are handlers that responds to requests from browsers and clients
# Handlers are written as Python Functions. 
# Each View Function is mapped to one or more request URLs.

from app import app

# Function to render the templates
from flask import render_template

# Import to use redirect and url_for methods
from flask import url_for, redirect

# Import Request object to use
from flask import request


@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def sigup():
    return render_template('signup.html')

@app.route('/login_validation',methods=['GET','POST'])
def login_validation():
	if request.method == "POST":
		userID = request.form['userid']
		password = request.form['loginpassword']
		# Can perform some password validation here!
		# return "Login Successful for: %s" % userID
	return render_template('home.html')



# ***************************************************************************

# @app.route('/home')
	# user = {'name': 'guest'}
	# posts = [
	# 	{
	# 		'author': {'name': 'user1'},
	# 		'question': 'The question 1 in detail.' 
	# 	},
	# 	{
	# 		'author': {'name': 'user2'},
	# 		'question': 'The question 2 in detail.' 
	# 	}
	# ]
	# return render_template('index.html',title='Home',user=user,posts=posts)

@app.route('/login/<name>')
def hello_name(name):
	return "Hello, %s!" % name

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/question/<int:questionID>')
def show_question(questionID):
	return "Question Number: %d" % questionID

@app.route('/admin')
def hello_admin():
	return "Hello Admin!"

@app.route('/ask')
def ask():
	return render_template('ask.html')

@app.route('/QueryNext',methods=['GET','POST'])
def QueryNext():
	# To find out the method of request, use 'request.method'
	if request.method == "GET":
		print(request.args)
		question = request.args.get("question")
	return "Query Successful!"
				
	# elif request.method == "POST":
	# 	userID = request.form['userid']
	# 	password = request.form['loginpassword']
	# 	# Can perform some password validation here!
	# 	return "Login Successful for: %s" % userID
	# Simple returns a string to the client

@app.route('/AddNext',methods=['GET','POST'])
def AddNext():
	# To find out the method of request, use 'request.method'
	if request.method == "GET":
		print(request.args)
		question = request.args.get("question")
		title = request.args.get("title")
		print(question)
		print(title)
	return "Question added Successfully!"
				
	# elif request.method == "POST":
	# 	userID = request.form['userid']
	# 	password = request.form['loginpassword']
	# 	# Can perform some password validation here!
	# 	return "Login Successful for: %s" % userID
	# Simple returns a string to the client 