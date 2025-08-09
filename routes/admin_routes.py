from flask import Blueprint, render_template, session, redirect, url_for, request
import pdfkit
import sqlite3
import os
from db.db_config import get_connection
from controllers.admin import (
    get_all_users,
    get_all_incidents,
    get_admin_logs,
    get_dashboard_stats,
    delete_user,
    update_incident_status,
    edit_user,
    log_admin_action,
    get_user_logs,
    delete_incident,
    export_incidents_as_csv, 
    filter_incidents
)

bp = Blueprint('admin_routes', __name__)

@bp.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('auth_routes.login'))

    keyword = request.args.get('search', '')
    incidents = filter_incidents(keyword)

    stats = get_dashboard_stats()
    users = get_all_users()
    logs = get_admin_logs()
    user_logs = get_user_logs()

    return render_template(
        'admin.html',
        stats=stats,
        users=users,
        logs=logs,
        user_logs=user_logs,
        incidents=incidents
    )

@bp.route('/admin/user/delete/<int:user_id>', methods=['POST'])
def delete_user_route(user_id):
    if session.get('role') != 'admin':
        return redirect(url_for('auth_routes.login'))
    delete_user(user_id)
    return redirect(url_for('admin_routes.admin_dashboard'))

@bp.route('/admin/user/edit/<int:user_id>', methods=['POST'])
def edit_user_route(user_id):
    if session.get('role') != 'admin':
        return redirect(url_for('auth_routes.login'))
    edit_user(user_id)
    return redirect(url_for('admin_routes.admin_dashboard'))

@bp.route('/admin/delete/<int:incident_id>', methods=['POST'])
def delete_incident_route(incident_id):
    delete_incident(incident_id)
    log_admin_action(session.get('username'), f"Deleted incident #{incident_id}")
    return redirect(url_for('admin_routes.admin_dashboard'))

@bp.route('/admin/edit/<int:incident_id>', methods=['GET', 'POST'])
def edit_incident(incident_id):
    if session.get('role') != 'admin':
        return redirect(url_for('auth_routes.login'))

    conn = get_connection()  # ✅ make sure we have a connection here

    if request.method == 'POST':
        new_status = request.form.get('status')

        cur = conn.cursor()
        cur.execute("UPDATE incidents SET status = ? WHERE id = ?", (new_status, incident_id))
        conn.commit()
        cur.close()

        log_admin_action(session.get('username'),
                         f"Updated status of incident #{incident_id} to {new_status}")

        conn.close()
        return redirect(url_for('admin_routes.admin_dashboard'))

    # GET request: fetch incident details
    cur = conn.cursor(dictionary=True)  # ✅ dictionary=True works for MySQL
    cur.execute("SELECT * FROM incidents WHERE id = ?", (incident_id,))
    incident = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('admin.html', incident=incident)


@bp.route('/admin/export/csv')
def export_csv():
    if session.get('role') != 'admin':
        return redirect(url_for('auth_routes.login'))
    return export_incidents_as_csv()


