    
import os
import uuid

from flask import Blueprint, flash, render_template, request, session, current_app, send_from_directory

from config import ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
from models.file import allowed_file, get_file, save_file_metadata
import logging
from models.file import get_files_by_user

logger = logging.getLogger(__name__)
upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload(): 
    if request.method == 'GET':
        return render_template('upload.html')

    if 'user' not in session: #check if the user is authenticated, unauthenticated users are not allowed to upload files
        return "Unauthorized", 401
    
    if 'file' not in request.files:
        logger.error("No file part in the request")
        flash("Please select a file to upload")
        return render_template('upload.html'), 400

    file = request.files['file']
    logger.info(f"File received: {file.filename}")

    if file.filename == '':
        logger.error("No selected file")
        flash("Please select a file to upload")
        return render_template('upload.html'), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename) #make filename safe
        unique_name = str(uuid.uuid4()) + "_" + filename

        try:
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
            file.save(path) #to avoid overwriting files with the same name, current_app is used to gain access to the active flask application
            logger.info(f"Saving file to: {path}")
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            flash (f"An error occurred while saving the file: {e}")
            return render_template('upload.html'), 500

        save_file_metadata(session['user'], filename, unique_name) #save metadata of the file in database
        logger.info(f"File {filename} uploaded successfully by user {session['user']}")

        return render_template('upload.html', message="File uploaded successfully!")
    else:
        logger.error(f"User attempted to upload invalid file: {file.filename}")
        return render_template('upload.html', message="Invalid file type. Allowed types are: " + ", ".join(ALLOWED_EXTENSIONS)), 400

@upload_bp.route('/download/<int:file_id>')
def download(file_id):

    if 'user' not in session:
        logger.error("Unauthorized download attempt")
        return "Unauthorized", 401

    file = get_file(file_id)

    if not file:
        logger.error(f"File with id {file_id} not found for user {session['user']}")
        return "File not found", 404
    
    if file[1] != session['user']:
        logger.error(f"User {session['user']} attempted to download file {file[2]} owned by {file[1]}")
        return "Forbidden", 403
    
    
    try:
        logger.info(f"User is downloading file {file[2]} with stored name {file[3]}")
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'],file[3])

        logger.info(f"Looking for file at: {filepath}")
        logger.info(f"Exists: {os.path.exists(filepath)}")
        return send_from_directory(
            current_app.config['UPLOAD_FOLDER'],
            file[3],
            as_attachment=True,
            download_name=file[2]
        )
    
    except Exception as e:
        logger.error(f"Download error: {e}")
        return str(e), 500
    

@upload_bp.route('/user_files')
def user_files():
    if 'user' not in session:
        logger.error("Unauthorized access to user files")
        return "Unauthorized", 401

    files = get_files_by_user(session['user'])
    return render_template('user_files.html', files=files)
