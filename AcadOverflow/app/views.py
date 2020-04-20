# Views are handlers that responds to requests from browsers and clients

# Handlers are written as Python Functions. 
# Each View Function is mapped to one or more request URLs.

from flask import render_template, flash, redirect, url_for, session, logging, request
from app import app
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime
from operator import attrgetter
import sys

sys.path.append("./app")
sys.path.append("./app/gql_client")

from gql_client.register_users import register_user
from gql_client.user_exists import user_exists
from gql_client.get_login_details import get_login_details
from gql_client.query_question_for_list import query_question_for_list
from gql_client.post_question import post_question
from gql_client.query_question_for_list import query_question_for_list

# Index
@app.route('/')
@app.route('/index')
def index():
	if 'logged_in' in session:
		return redirect(url_for('home'))
	return render_template('index.html')

# Check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			# flash('Unauthorized, Please login', 'danger')
			return redirect(url_for('login'))
	return wrap

# Register Form Class
class RegisterForm(Form):
	fname = StringField('FirstName', [validators.Length(min=1, max=50)])
	lname = StringField('LastName', [validators.Length(min=1, max=50)])
	emailId = StringField('EmailId', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match!! Try Again.')
	])
	confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
	# form = RegisterForm(request.form)
	if request.method == 'POST':
		emailId = request.form['emailId']

		if user_exists(emailId):
			flash ('Already registered with emailId: {}!!'.format(emailId), 'danger')
			return render_template('register.html')

		fname = request.form['fname']
		lname = request.form['lname']

		# check entered passwords
		password = sha256_crypt.encrypt(request.form['password'])
		confirm_password = request.form['confirm_password']

		if not sha256_crypt.verify(confirm_password, password):
			flash('Passwords do not match!!', 'danger')
			return redirect(url_for('register'))

		try:
			register_user(emailId, fname, lname, password)
			flash('{} registered!! Please log in'.format(emailId), 'success')
			return redirect(url_for('login'))
		except Exception as e:
			print(e)
			flash('Something went wrong!! Please try again', 'danger')

	return render_template('register.html')


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'logged_in' in session:
		return redirect(url_for('home'))

	if request.method != 'POST':
		return render_template('login.html')

	# Get Form Fields
	emailId = request.form['emailId']
	password_candidate = request.form['password']
	
	user = get_login_details(emailId)
	if not user:
		error = 'EmailId: {} not registered!!'.format(emailId)
		return render_template('login.html', error=error)

	password = user["Password"]
	fname = user["FirstName"]
	lname = user["LastName"]

	# Compare Passwords
	if not sha256_crypt.verify(password_candidate, password):
		error = 'Incorrect Passord!!'
		return render_template('login.html', error=error)

	# Passed
	session['logged_in'] = True
	session['userId'] = int(user["Id"])
	session['emailId'] = emailId
	session['fname'] = fname
	session['lname'] = lname
	session['profile_img'] = fname + ".jpg"

	return redirect(url_for('home'))


# Logout
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('index'))

@app.route('/home')
@is_logged_in
def home():
	return render_template('home.html')

@app.route('/ask_question')
def ask_question():
	return render_template('ask_question.html')

@app.route('/AddQuestionNext',methods=['GET','POST'])
def AddQuestionNext():
	# To find out the method of request, use 'request.method'
	if request.method == "GET":
		title = request.args.get("title")
		body = request.args.get("body")
		tags_list = ['tag1', 'tag2']
		userId = session['userId']
		post_question(title, body, tags_list, userId)
		return "Question added with title : %s" % title
			
	elif request.method == "POST":
		title = request.form['title']
		body = str(request.form['body'])
		tags_list = ['tag1', 'tag2']
		userId = session['userId']
		post_question(title, body, tags_list,userId)
		flash("Question Posted successfully", "success")
		return redirect(url_for('home'))
	

@app.route('/SearchQuestionNext',methods=['GET','POST'])
def SearchQuestionNext():
	# To find out the method of request, use 'request.method'
	if request.method == "GET":
		print(request.args)
		question = request.args.get("question")
		print(question)				
	elif request.method == "POST":
		question = request.form['question']
		return "Question Searching: %s" % question
	return "Question searched successfully"

