from flask import Flask

import os

from config import UPLOAD_FOLDER, SECRET_KEY, MAX_CONTENT_LENGTH


app = Flask(__name__)

app.secret_key = SECRET_KEY

app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER # Set the upload folder path relative to the app directory
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH #set max file size to 16MB
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) #create the uploads folder if it doesn't exist


if __name__ == '__main__':
    app.run(debug=True)