import sqlite3
import os

# Path where the SQlite database will be stored inside the container
DB_PATH = "/data/auth.db"

def connect_db():
    """
    Create and return connection to SQlite database
    Returns SQlite connection that allows interaction with the database
    """
    return sqlite3.connect(DB_PATH)

def init_db():
    """
    Initializes the database.
    This function creates a users table if it does not already exists.
    It stores username and password.
    """
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
    """
    Insert a new user into the database.
    param: username:str,
    param: password:str
    returns: bool. True if user is successfully created and False if the user already exist.
    """
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
    """
    Retrieve a user's password from the database.
    param: username:str
    return: tuple or None. Returns a tuple containing the password is the user exists and otherwise
    it returns None.
    """
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
    """
    Update the password of an existing user.
    param: username:str
    param: new_password:str, which will replace the old password.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        (new_password, username)
    )
    conn.commit()
    conn.close()