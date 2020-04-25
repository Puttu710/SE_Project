# Views are handlers that responds to requests from browsers and clients

# Handlers are written as Python Functions. 
# Each View Function is mapped to one or more request URLs.

from flask import render_template, flash, redirect, url_for, session, logging, request
from flask_sqlalchemy import SQLAlchemy
import os
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
from app import app
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime
from operator import attrgetter
import sys

from gql_client.register_users import register_user
from gql_client.user_exists import user_exists
from gql_client.get_login_details import get_login_details
from gql_client.query_question_for_list import query_question_for_list
from gql_client.post_question import post_question
from gql_client.query_question_for_list import query_question_for_list

# from ml_module.search import searchresults, predict_tags

basedir = os.path.abspath(os.path.dirname(__file__))

# Configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Modules
db = SQLAlchemy(app)

class Users (db.Model):
	__tablename__ = 'users'
	Id = db.Column(db.Integer, primary_key=True)
	FirstName = db.Column(db.String(40))
	LastName = db.Column(db.String(40))
	EmailId = db.Column(db.String(256), unique=True)
	Password = db.Column(db.String(256))
	created_at = db.Column(db.DateTime)
	questions = db.relationship('Questions', backref='question_author')
	answers = db.relationship('Answers', backref='answer_author')

	def __repr__(self):
		return '<User {}>'.format(self.EmailId)

class Questions (db.Model):
	__tablename__ = 'questions'
	Id = db.Column(db.Integer, primary_key=True)
	Title = db.Column(db.Text, unique=True)
	VoteCount = db.Column(db.Integer, default=0)
	UserId = db.Column(db.Integer, db.ForeignKey('users.Id'))
	created_at = db.Column(db.DateTime)
	Tags = db.Column(db.String(256))
	Body = db.Column(db.Text, nullable=True)
	post_corpus = db.Column(db.Text, nullable=True)
	question_url = db.Column(db.String(256), nullable=True)
	overall_scores = db.Column(db.Float, nullable=True)
	sentiment_polarity = db.Column(db.Float, nullable=True)
	sentiment_subjectivity = db.Column(db.Float, nullable=True)
	answers = db.relationship('Answers', backref='question')

	def __repr__(self):
		return '<QuesId {}>'.format(self.Id)

class Answers (db.Model):
	__tablename__ = 'answers'
	Id = db.Column(db.Integer, primary_key=True)
	VoteCount = db.Column(db.Integer, default=0)
	QuestionId = db.Column(db.Integer, db.ForeignKey('questions.Id'))
	Body = db.Column(db.Text, unique=True)
	UserId = db.Column(db.Integer, db.ForeignKey('users.Id'))
	created_at = db.Column(db.DateTime)

	def __repr__(self):
		return '<AnsId {}>'.format(self.Id)


class UserObject(SQLAlchemyObjectType):
   class Meta:
       model = Users
       interfaces = (graphene.relay.Node, )

class QuestionObject(SQLAlchemyObjectType):
    class Meta:
        model = Questions
        interfaces = (graphene.relay.Node, )

class AnswerObject(SQLAlchemyObjectType):
    class Meta:
        model = Answers
        interfaces = (graphene.relay.Node, )


# Queries
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserObject)
    all_questions = SQLAlchemyConnectionField(QuestionObject)
    all_answers = SQLAlchemyConnectionField(AnswerObject)

    user_email_id = graphene.Field(UserObject, EmailId=graphene.String())
    question_with_id = graphene.Field(QuestionObject, Id=graphene.Int())

    def resolve_user_email_id(self, info, EmailId):
        return Users.query.filter_by(EmailId=EmailId).first()

    def resolve_question_with_id(self, info, Id):
        return Questions.query.filter_by(Id=Id).first()


# Mutations
class CreateUser(graphene.Mutation):
    class Arguments:
        FirstName = graphene.String(required=True)
        LastName = graphene.String(required=True)
        EmailId = graphene.String(required=True)
        Password = graphene.String(required=True)

    user = graphene.Field(lambda: UserObject)

    def mutate(self, info, EmailId, FirstName, LastName, Password):
        user = Users(EmailId=EmailId, FirstName=FirstName, LastName=LastName, Password=Password)

        db.session.add(user)
        db.session.commit()
        return CreateUser(user=user)


class CreateQuestion(graphene.Mutation):
    class Arguments:
        Title = graphene.String(required=True)
        UserId = graphene.Int(required=True)
        Tags = graphene.String(required=True)
        Body = graphene.String(required=False)
        post_corpus = graphene.String(required=False)
        question_url = graphene.String(required=False)
        overall_scores = graphene.Float(required=False)
        sentiment_polarity = graphene.Float(required=False)
        sentiment_subjectivity = graphene.Float(required=False)

    question = graphene.Field(lambda: QuestionObject)

    def mutate(self, info, Title, post_corpus, Body, question_url, Tags, overall_scores, \
                     sentiment_polarity, sentiment_subjectivity, UserId):
        user = Users.query.filter_by(Id=UserId).first()
        question = Questions(Title=Title, post_corpus=post_corpus, Body=Body, question_url=question_url, Tags=Tags, \
		                 overall_scores=overall_scores, sentiment_polarity=sentiment_polarity, sentiment_subjectivity=sentiment_subjectivity)
        question.question_author = user

        db.session.add(question)
        db.session.commit()
        return CreateQuestion(question=question)


class CreateAnswer(graphene.Mutation):
    class Arguments:
        Body = graphene.String(required=True)
        UserId = graphene.Int(required=True)
        QuestionId = graphene.Int(required=True)

    answer = graphene.Field(lambda: AnswerObject)

    def mutate(self, info, QuestionId, Body, UserId):
        user = Users.query.filter_by(Id=UserId).first()
        question = Questions.query.filter_by(Id=QuestionId).first()
        answer = Answers(Body=Body, QuestionId=QuestionId, UserId=UserId)
        answer.answer_author = user
        answer.question = question

        db.session.add(answer)
        db.session.commit()
        return CreateAnswer(answer=answer)


class QuestionVoteCountMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        Id = graphene.Int(required=True)
        val = graphene.Int(required=True)

    question = graphene.Field(QuestionObject)

    def mutate(self, info, Id, val):
        question = Questions.query.filter_by(Id=Id).first()
        question.VoteCount += val
        db.session.add(question)
        db.session.commit()
        return QuestionVoteCountMutation(question=question)

class AnswerVoteCountMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        Id = graphene.Int(required=True)
        val = graphene.Int(required=True)

    answer = graphene.Field(AnswerObject)

    def mutate(self, info, Id, val):
        answer = Answers.query.filter_by(Id=Id).first()
        answer.VoteCount += val
        db.session.add(answer)
        db.session.commit()
        return QuestionVoteCountMutation(answer=answer)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_question = CreateQuestion.Field()
    create_answer = CreateAnswer.Field()

    update_question_votecount = QuestionVoteCountMutation.Field()
    update_answer_votecount = QuestionVoteCountMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True    # for having the GraphiQL interface
    )
)

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
		post_question(title, body, tags_list, userId)
		flash("Question Posted successfully.", "success")
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

