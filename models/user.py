
from datetime import datetime, timedelta
import re
import uuid
from config import DATABASE
import sqlite3
import uuid
import bcrypt
import logging

logger = logging.getLogger(__name__)

def is_valid_name_input(username):
    # Define the pattern for a valid username 
    pattern = r'^[a-zA-Z0-9_-]{4,20}$'

    # Use re.match to check if the provided username matches the pattern
    if re.match(pattern, username):
        return True
    else:
        return False  

# Create a new user
def create_user(username, password):
    hashed_password = hash_password(password)
    token = str(uuid.uuid4())
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, token) VALUES (?, ?, ?)', 
                       (username, hashed_password, token))
        conn.commit()
        logger.info(f"User {username} successfully created")
    except sqlite3.Error as e:
        logger.error(f"Error creating user {username}: {e}")
        raise #raise the exception to be handled by the calling function
    finally:
        conn.close()


def verify_password(username, password):
    logger.info(f"Attempting to verify password for user: {username}")
    try:            
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE username=?', (username,) #? makes it so that the username is treated as a parameter, preventing SQL injection attacks
            )
        user = cursor.fetchone()                                                   
    except sqlite3.Error as e:
        logger.error(f"Error retrieving user {username}: {e}")
        raise
    finally:
        conn.close() 

    if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        logger.info(f"Password verified for user: {username}")
        return user
    logger.warning(f"Password verification failed for user: {username}")
    return None

# Hash a password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def save_reset_token(username, token, expiration):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET reset_token=?, reset_token_expiration=? WHERE username=?', (token, expiration.isoformat(), username))
        conn.commit()
        logger.info(f"Reset token saved for user {username} with expiration {expiration.isoformat()}")
    except sqlite3.Error as e:
        logger.error(f"Error saving reset token for user {username}: {e}")
        raise
    finally:
        conn.close()


def token_expired(user):
    expired = datetime.fromisoformat(user[6])
    return datetime.now() > expired

def update_password(id, new_password):
    hashed_pass = hash_password(new_password)
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET password=? WHERE id=?', (hashed_pass, id))
        conn.commit()
        logger.info(f"Password updated for user with id {id}")
    except sqlite3.Error as e:
        logger.error(f"Error updating password for user with id {id}: {e}")
        raise
    finally:
        conn.close()


def invalidate_token(username):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET reset_token=NULL, reset_token_expiration=NULL WHERE username=?', (username,))
        conn.commit()
        logger.info(f"Reset token sucessfully invalidated for user {username}")
    except sqlite3.Error as e:
        logger.error(f"Error invalidating token for user {username}: {e}")
        raise
    finally:
        conn.close()


def get_user_by_token(token):
    try:
        conn = sqlite3.connect(DATABASE) #connect to database 
        cursor = conn.cursor() #create a cursor object to execute SQL queries
        cursor.execute('SELECT * FROM users WHERE reset_token=?', (token,)) #use reset token to select user
        user = cursor.fetchone() #retrieve the first row of the result set
        logger.info(f"User retrieved by token: {token}")
    except sqlite3.Error as e:
        logger.error(f"Error retrieving user by token {token}: {e}")
        raise
    finally:
        conn.close() #close the database connection
    return user

# def get_all_users():
#     logger.info("Retrieving all users from the database")
#     try:
#         conn = sqlite3.connect(DATABASE)
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT id, username, Role FROM users"
#         )
#         users = cursor.fetchall()
#     except sqlite3.Error as e:
#         logger.error(f"Error retrieving users: {e}")
#         raise
#     finally:
#         conn.close()
#     return users