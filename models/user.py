
import uuid
from config import DATABASE
import sqlite3
import uuid
import bcrypt

# Create a new user
def create_user(username, password):
    hashed_password = hash_password(password)
    token = str(uuid.uuid4())
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, token) VALUES (?, ?, ?)', (username, hashed_password, token))
    conn.commit()
    conn.close()


def verify_password(username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM users WHERE username=?', (username,)
        )
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        return user
    return None

# Hash a password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')