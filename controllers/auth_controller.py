
from flask import Blueprint, app, flash, jsonify, redirect, render_template, request, session, url_for, g
import sqlite3
from models.user import verify_password, create_user
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

auth_bp = Blueprint('auth', __name__) #using blueprint, which allows for modular organization so that routes can be grouped together in controllers folder instead of having all the routes be in app.py

@auth.verify_password
def authenticate(username, password):
    try:
        g.user = verify_password(username, password)
        return g.user
    except Exception as e:
        print(e)
        return None

# API route to get user information
@auth_bp.route('/api/userinfo')
@auth.login_required
def get_user_info():
    user = g.user
    return jsonify({'id': user[0], 'username': user[1]})

@auth_bp.route('/api/admin')
@auth.login_required
def admin():
    user = g.user
    if user[4] == 'admin':
        return jsonify({'message': 'Welcome, admin!'})
    else:
        return jsonify({'message': 'Access denied. Admins only.'}), 403

@auth_bp.route('/api/files')
@auth.login_required
def get_files():
    user = g.user
    return jsonify({'message': f'Here are the files for {user[1]}'})

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form['username']
    password = request.form['password']

    try:
        create_user(username, password)
        flash("Registration successful! Please log in.") #display message on the login page
        return redirect(url_for('auth.login'))
    except sqlite3.IntegrityError:
        flash("Username already exists. Please choose a different username.") #display a message on the registration page if the username already exists
        return render_template('register.html') 



@auth_bp.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    user = verify_password(username, password)

    if user:
        session['user'] = username
        return redirect(url_for('upload.upload'))

    flash("Invalid username or password. Please try again.") #display message on login page
    return redirect(url_for('auth.login'))

@auth_bp.route('/')
def login():
    return render_template('login.html')    