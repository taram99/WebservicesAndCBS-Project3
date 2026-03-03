import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "shortening_service.db")

def connect_db():
    return sqlite3.connect(DB_PATH)

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
    conn.close()

def get_id_by_url(url): #check if url exists
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM urls WHERE url = ?", (url,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def inser_new_url(short_id, url, owner):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls (id, url, clicks, owner) VALUES (?, ?, ?, ?)",
        (short_id, url, 0, owner)
    )
    conn.commit()
    conn.close()

def ids_user(owner): #get ids for user/owner
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM urls WHERE owner = ?", (owner,))
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def url_row(short_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT url, clicks, owner FROM urls WHERE id = ?", (short_id,))
    row = cursor.fetchone()
    conn.close()
    return row 

def increment_clicks(short_ids):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE urls SET clicks = clicks + 1 WHERE id = ?", (short_id,))
    conn.commit()
    conn.close()

def update_url_in_db(short_id, new_url):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE urls SET url = ?, clicks = 0 WHERE id = ?",
        (new_url, short_id)
    )
    conn.commit()
    conn.close()

def delete_url(short_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM urls WHERE id = ?", (short_id,))
    conn.commit()
    conn.close()

def does_url_exist(url,current_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM urls WHERE url = ? AND id != ?", (url, current_id))
    row = cursor.fetchone()
    conn.close()
    return row is not None