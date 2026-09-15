from config import ALLOWED_EXTENSIONS, DATABASE
import sqlite3
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file_metadata(username, original_filename, stored_filename): #save the metadata of a file in the database
    try: 
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO files
            (
                username,
                original_filename,
                stored_filename,
                upload_date
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                username,
                original_filename,
                stored_filename,
                datetime.now().isoformat()
            )
        )
        conn.commit()
    except Exception as e:
        logger.error(f"Error saving file metadata: {e}")
        raise
    finally:
        conn.close()


def get_file(file_id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM files
            WHERE id=?
            """,
            (file_id,)
        )
        file = cursor.fetchone()
    except Exception as e:
        logger.error(f"Error retrieving file: {e}")
        raise
    finally:
        conn.close()
    return file


def get_files_by_user(username):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM files
            WHERE username=?
            """,
            (username,)
        )
        files = cursor.fetchall() #fetches all files associated with the given username
    except Exception as e:
        logger.error(f"Error retrieving user files: {e}")
        raise
    finally:
        conn.close()
    return files