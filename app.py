from flask import Flask, jsonify

import os

from config import UPLOAD_FOLDER, SECRET_KEY, MAX_CONTENT_LENGTH
from models.database import init_db


app = Flask(__name__)

app.secret_key = SECRET_KEY

init_db() #initialize the database and create the users table if it doesn't exist

app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER # Set the upload folder path relative to the app directory
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH #set max file size to 16MB
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) #create the uploads folder if it doesn't exist

from controllers.auth_controller import auth_bp
app.register_blueprint(auth_bp) #import the auth blueprint and register it in the app

from controllers.upload_controller import upload_bp
app.register_blueprint(upload_bp) #import the upload blueprint and register it in the app

if __name__ == '__main__':
    app.run(debug=True)

