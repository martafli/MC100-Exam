import sqlite3

from config import DATABASE


# Initialize the database and create the users table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            token TEXT,
            Role TEXT DEFAULT 'user'
        )
    ''')
    conn.commit()
    conn.close()

init_db()