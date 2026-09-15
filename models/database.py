import sqlite3

from config import DATABASE
import logging

logger = logging.getLogger(__name__)


# Initialize the database and create the users table if it doesn't exist
def init_db():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                token TEXT,
                Role TEXT DEFAULT 'user',
                reset_token TEXT,
                reset_token_expiration TEXT
            )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            original_filename TEXT,
            stored_filename TEXT,
            upload_date TEXT
            )
        ''')
        conn.commit()
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
    finally:
        conn.close()