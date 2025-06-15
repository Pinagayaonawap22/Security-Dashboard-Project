from db.db_config import get_connection

def log_user_action(user_id, username, role, action, status="Success"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_logs (user_id, username, role, action, status)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, username, role, action, status))
    conn.commit()
    cur.close()
    conn.close()
