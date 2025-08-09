from db.db_config import get_connection
import sqlite3  
import os

def log_user_action(user_id, username, role, action, status="Success"):
    conn = get_connection()
    cur = conn.row_factory = sqlite3.Row
    cur.execute("""
        INSERT INTO user_logs (user_id, username, role, action, status)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, username, role, action, status))
    conn.commit()
    cur.close()
    conn.close()
