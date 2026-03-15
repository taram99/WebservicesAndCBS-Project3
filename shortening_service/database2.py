import sqlite3
import os

# Path to SQlite database used by shortening service
DB_PATH = "/data/shortening_service.db"

def connect_db():
    """
    Create and return connection to SQlite database
    Returns SQlite connection that allows interaction with the database
    """
    return sqlite3.connect(DB_PATH)

def init_db():
    """
    Initializes the database.
    This function creates the urls table if it does not already exists.
    It stores shortened urls and their metadata.
    """
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

def get_id_by_url(url): 
    """
    Retrieves the short ID associated with a given url.
    param: url:str, the original url to search for.
    returns: str or None. The short ID if the url exists in the database.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM urls WHERE url = ?", (url,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def insert_new_url(short_id, url, owner):
    """
    Insert a new shortened url, record into the database.
    param: short_id:str, the generated short identifier,
    param: url: str, the original url that will be shortened,
    param: owner: str, username of the user who owns the link.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls (id, url, clicks, owner) VALUES (?, ?, ?, ?)",
        (short_id, url, 0, owner)
    )
    conn.commit()
    conn.close()

def ids_user(owner): 
    """
    Retrieves all shortened url IDs created by a specific user.
    param: owner: str, username of the owner
    returns: list[str], list of short IDs belonging to the user.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM urls WHERE owner = ?", (owner,))
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def url_row(short_id):
    """
    Retrieves the url record associated with a short ID.
    param: short_id:str, the short identifier.
    returns: tuple or None. Tuple contains the url, clicks, owner if the record exists.
    None if the ID is not found.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT url, clicks, owner FROM urls WHERE id = ?", (short_id,))
    row = cursor.fetchone()
    conn.close()
    return row 

def increment_clicks(short_id):
    """
    Increase the click counter for a shortened url.
    param: short_id: str, the short identifier whose click count should be incremented.
    """
    conn = connect_db()
    cursor = conn.cursor()
    #Increase click count by 1
    cursor.execute("UPDATE urls SET clicks = clicks + 1 WHERE id = ?", (short_id,))
    conn.commit()
    conn.close()

def update_url_in_db(short_id, new_url):
    """
    Update the original url associated with a short ID.
    The click counter is reset to 0 when the url changes.
    param: short_id:str, the identifier of the shortened url.
    param: new_url: str, the updated destination url.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE urls SET url = ?, clicks = 0 WHERE id = ?",
        (new_url, short_id)
    )
    conn.commit()
    conn.close()

def delete_url_db(short_id):
    """
    Delete a shortened url from the database.
    param: short_id: str, the identifier of the shortened url that should be removed.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM urls WHERE id = ?", (short_id,))
    conn.commit()
    conn.close()

def does_url_exist(url,current_id):
    """
    Checks whether a url already exists in the database under a different short ID to avoid 
    duplicates.
    param: url:str, the url to check,
    param: current_id: str, the current short ID (excluded from the search).
    returns: bool. True if the url already exists with a different ID, False otherwise.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM urls WHERE url = ? AND id != ?", (url, current_id))
    row = cursor.fetchone()
    conn.close()
    return row is not None