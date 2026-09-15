
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for, g
import sqlite3
from models.file import get_file_by_user
from models.user import verify_password, create_user, save_reset_token, token_expired, update_password, invalidate_token, get_user_by_token
from flask_httpauth import HTTPBasicAuth
import secrets
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

auth = HTTPBasicAuth()

auth_bp = Blueprint('auth', __name__) #using blueprint, which allows for modular organization so that routes can be grouped together in controllers folder instead of having all the routes be in app.py

@auth.verify_password
def authenticate(username, password):
    try:
        g.user = verify_password(username, password)
        return g.user
    except Exception as e:
        logger.error(f"Error during authentication: {e}")
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
    files = get_file_by_user(user[1])

    return jsonify({
    'from user': user[1],
    'files': [
        {
            'filename': file[2],
            'upload_date': file[4]
        }
        for file in files
    ]
})

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form['username']
    password = request.form['password']
    logger.info(f"Attempting to register user: {username}")

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

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')
    username = request.form['username']
    token = secrets.token_urlsafe(32) # Generate a secure token
    expiration = datetime.now() + timedelta(minutes=10) # Set expiration time to 10 min
    save_reset_token(username, token, expiration) # Save the token and expiration in the database

    return redirect(url_for('auth.reset_password', token=token))  # Redirect to the reset password page with the token"

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST']) 
def reset_password(token):

    user = get_user_by_token(token)
    if not user:
        return "Invalid token"
    elif token_expired(user):
        return "Token has expired"

    if request.method == 'GET':
            return render_template('reset_password.html')
    
    new_password = request.form['password']
    update_password(user[0], new_password)  # Update the password in the database
    logger.info(f"Password updated for user with id {user[0]}")
    invalidate_token(user[0])  # Invalidate the token after use
    flash ("Password reset successful!") #display message on login page
    return redirect(url_for('auth.login'))  