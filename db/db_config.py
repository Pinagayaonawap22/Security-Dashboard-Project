import sqlite3
import os

def get_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "local_database.sqlite")

    # Debug
    print("[DB DEBUG] Using SQLite at:", db_path)

    return sqlite3.connect(db_path)
