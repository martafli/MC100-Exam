    
import os
import uuid

from flask import app, render_template, request, session

from config import ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
from models.file import allowed_file


@app.route('/upload', methods=['GET', 'POST'])
def upload(): 
    if request.method == 'GET':
        return render_template('upload.html')

    if 'user' not in session: #check if the user is authenticated, unauthenticated users will not have the role 'user'
        return "Unauthorized", 401
    
    if 'file' not in request.files:
        return render_template('upload.html', message="No file part in the request")

    file = request.files['file']

    if file.filename == '':
        return render_template('upload.html', message="No selected file")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename) #make filename safe
        unique_name = str(uuid.uuid4()) + "_" + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name)) #to avoid overwriting files with the same name
        return render_template('upload.html', message="File uploaded successfully")
    else:
        return render_template('upload.html', message="Invalid file type. Allowed types are: " + ", ".join(ALLOWED_EXTENSIONS)), 400
        