import csv
from flask import make_response
from db.db_config import get_connection
from io import StringIO

def get_all_users():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, username, role, email FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def get_admin_logs():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM admin_logs ORDER BY created_at DESC")
    logs = cur.fetchall()
    cur.close()
    conn.close()
    return logs

def delete_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

def edit_user(user_id):
    # Placeholder — later you can use a form to update name/role
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET role = 'analyst' WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    
def get_dashboard_stats():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # ✅ Use correct table: incidents
    cur.execute("SELECT COUNT(*) AS total FROM incidents")
    total_incidents = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM incidents WHERE severity = 'Critical'")
    critical_incidents = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM incidents WHERE status = 'Resolved'")
    resolved_incidents = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM users")
    total_users = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM admin_logs")
    total_logs = cur.fetchone()['total']

    cur.close()
    conn.close()

    return {
        'total_incidents': total_incidents,
        'critical': critical_incidents,
        'resolved': resolved_incidents,
        'total_users': total_users,
        'logs': total_logs
    }

def get_admin_logs():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT username, action, created_at, status FROM admin_logs ORDER BY created_at DESC")
    logs = cur.fetchall()
    cur.close()
    conn.close()
    return logs

def get_all_incidents():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, title, type, severity, status, date FROM incidents ORDER BY date DESC")
    incidents = cur.fetchall()
    cur.close()
    conn.close()
    return incidents

def log_admin_action(username, action, status="Success"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO admin_logs (username, action, status) VALUES (%s, %s, %s)",
        (username, action, status)
    )
    conn.commit()
    cur.close()
    conn.close()
    
def get_user_logs():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT username, role, action, status, timestamp FROM user_logs ORDER BY timestamp DESC")
    logs = cur.fetchall()
    cur.close()
    conn.close()
    return logs


def get_all_incidents():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM incidents ORDER BY date DESC")
    incidents = cur.fetchall()
    cur.close()
    conn.close()
    return incidents

def update_incident_status(incident_id, new_status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE incidents SET status = %s WHERE id = %s", (new_status, incident_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_incident(incident_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM incidents WHERE id = %s", (incident_id,))
    conn.commit()
    cur.close()
    conn.close()

def filter_incidents(keyword=None):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    if keyword:
        query = """
            SELECT * FROM incidents
            WHERE title LIKE %s OR type LIKE %s OR severity LIKE %s OR status LIKE %s
            ORDER BY date DESC
        """
        wildcard = f"%{keyword}%"
        cur.execute(query, (wildcard, wildcard, wildcard, wildcard))
    else:
        cur.execute("SELECT * FROM incidents ORDER BY date DESC")

    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def export_incidents_as_csv():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Title', 'Type', 'Severity', 'Status'])

    data = get_all_incidents()
    for row in data:
        writer.writerow([row['date'], row['title'], row['type'], row['severity'], row['status']])

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=incidents.csv"
    response.headers["Content-type"] = "text/csv"
    return response
