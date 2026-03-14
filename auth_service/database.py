import os
import psycopg2
from psycopg2 import IntegrityError

#postgres connection
DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
DB_NAME = os.environ.get("DB_NAME", "webservices")
DB_USER = os.environ.get("DB_USER", "user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")

def connect_db():
        return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

def init_db():
    conn = connect_db()
    cursor = conn.cursor() #create cursor object
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
            )
            """)

    conn.commit() #apply change to database
    cursor.close() #close cursor when no longer in use
    conn.close() #close database connection when no longer in use


def creating_user_db(username, password): #inserting data
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password)  VALUES (%s, %s)",
                       (username, password)
                       )
        conn.commit()
        return True
    except IntegrityError:
        conn.rollback() #rollback transaction if error occurs
        return False
    finally:
        cursor.close()
        conn.close()

def get_user(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password FROM users WHERE username = %s",
        (username,)
    )
    result = cursor.fetchone() #if query returns one row
    cursor.close()
    conn.close()
    return result

def update_password_db(username, new_password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password = %s WHERE username = %s",
        (new_password, username)
    )
    conn.commit()
    cursor.close()
    conn.close()