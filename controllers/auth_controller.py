
from flask import app, flash, redirect, render_template, request, session, url_for
import sqlite3
from models.user import verify_password, create_user
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def authenticate(username, password):
    return verify_password(username, password)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form['username']
    password = request.form['password']

    try:
        create_user(username, password)
        flash("Registration successful! Please log in.") #display message on the login page
        return redirect(url_for('login'))
    except sqlite3.IntegrityError:
        flash("Username already exists. Please choose a different username.") #display a message on the registration page if the username already exists
        return render_template('register.html') 


@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    user = verify_password(username, password)

    if user:
        session['user'] = username
        return redirect(url_for('upload'))

    flash("Invalid username or password. Please try again.") #display message on login page
    return redirect(url_for('login'))

@app.route('/')
def login():
    return render_template('login.html')    