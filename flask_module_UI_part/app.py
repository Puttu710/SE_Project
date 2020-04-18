from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
# from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Index
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/signup')
def sigup():
    return render_template('signup.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login_validation',methods=['POST'])
def login_validation():
    username = request.form.get('username')
    password = request.form.get('password')
    return "the email is {} and the password is {}".format(username,password)

if __name__ == '__main__':
    app.run(debug=True)
