from db.db_config import get_connection
import sqlite3
import os

def get_all_reports():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM analyst_reports ORDER BY created_at DESC")
    reports = cur.fetchall()
    cur.close()
    conn.close()
    return reports

def submit_report(title, content):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO analyst_reports (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    cur.close()
    conn.close()
    
def submit_incident(title, severity, incident_type, system, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO incidents (title, type, severity, system, description, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, incident_type, severity, system, description, "In Progress"))
    conn.commit()
    cur.close()
    conn.close()

def get_all_incidents():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            id,
            title,
            type,
            severity,
            status,
            date
        FROM incidents
        ORDER BY date DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return [dict(row) for row in rows]  # ✅ Convert Row objects to dicts

def log_user_action(user_id, username, role, action, status="Success"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_logs (user_id, username, role, action, status)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, username, role, action, status))
    conn.commit()
    cur.close()
    conn.close()

def get_incident_stats():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            COUNT(*) AS total,
            SUM(CASE WHEN severity = 'Critical' THEN 1 ELSE 0 END) AS critical,
            SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
            SUM(CASE WHEN status = 'Resolved' THEN 1 ELSE 0 END) AS resolved
        FROM incidents
    """)
    stats = cur.fetchone()
    cur.close()
    conn.close()
    return stats

def read_incident_log():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, type, severity, status, date
        FROM incidents
        ORDER BY date DESC
    """)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def update_incident_status(incident_id, new_status):
    conn = get_connection()  # ✅ Get connection first
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        UPDATE incidents
        SET status = ?
        WHERE id = ?
    """, (new_status, incident_id))
    conn.commit()
    cur.close()
    conn.close()
