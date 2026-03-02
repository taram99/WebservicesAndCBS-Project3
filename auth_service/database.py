import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "auth.db")

def connect_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = connect_db()
    cursor = conn.cursor() #create cursor object
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
            )
            """)

    conn.commit() #apply change to database
    conn.close() #close database connection when no longer in use


def creating_user_db(username, password): #inserting data
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password)  VALUES (?, ?)",
                       (username, password)
                       )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )
    result = cursor.fetchone() #if query returns one row
    conn.close()
    return result

def update_password_db(username, new_password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        (new_password, username)
    )
    conn.commit()
    conn.close()