import os


DATABASE = 'user_database.db'

SECRET_KEY = os.urandom(24) # Generate a random secret key for session management
    
# Define the folder where uploaded files will be stored
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),'uploads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 #set max file size to 16MB


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}