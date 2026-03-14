import psycopg2
import os

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
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS urls (
                   id TEXT PRIMARY KEY,
                   url TEXT NOT NULL,
                   clicks INTEGER NOT NULL,
                   owner TEXT NOT NULL
                   )
            """)
    conn.commit()
    cursor.close()
    conn.close()

def get_id_by_url(url): #check if url exists
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM urls WHERE url = %s", (url,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row[0] if row else None

def insert_new_url(short_id, url, owner):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls (id, url, clicks, owner) VALUES (%s, %s, %s, %s)",
        (short_id, url, 0, owner)
    )
    conn.commit()
    cursor.close()
    conn.close()

def ids_user(owner): #get ids for user/owner
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM urls WHERE owner = %s", (owner,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [r[0] for r in rows]

def url_row(short_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT url, clicks, owner FROM urls WHERE id = %s", (short_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row 

def increment_clicks(short_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE urls SET clicks = clicks + 1 WHERE id = %s", (short_id,))
    conn.commit()
    cursor.close()
    conn.close()

def update_url_in_db(short_id, new_url):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE urls SET url = %s, clicks = 0 WHERE id = %s",
        (new_url, short_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

def delete_url_db(short_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM urls WHERE id = %s", (short_id,))
    conn.commit()
    cursor.close()
    conn.close()

def does_url_exist(url,current_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM urls WHERE url = %s AND id != %s", (url, current_id))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row is not None