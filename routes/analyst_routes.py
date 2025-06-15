# routes/analyst_routes.py
from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify 
from controllers.analyst import get_incident_stats, submit_incident, get_all_incidents, log_user_action

bp = Blueprint('analyst_routes', __name__)

@bp.route('/analyst/dashboard')
def analyst_dashboard():
    if session.get('role') != 'analyst':
        return redirect(url_for('auth_routes.login'))
    stats = get_incident_stats()
    incidents = get_all_incidents()  # Optional: show incident log on load
    return render_template('analyst.html',stats=stats, incidents=incidents)

@bp.route('/analyst/submit', methods=['POST'])
def analyst_submit_incident():
    if session.get('role') != 'analyst':
        return redirect(url_for('auth_routes.login'))

    title = request.form['title']
    severity = request.form['severity']
    incident_type = request.form['type']
    system = request.form['system']
    description = request.form['description']

    # Store incident
    submit_incident(title, severity, incident_type, system, description)

    # Log action
    log_user_action(
        user_id=None,
        username=session.get('username'),
        role=session.get('role'),
        action=f"Submitted incident: {title}",
        status="Success"
    )

    # ✅ Add this to return a proper response
    return redirect(url_for('analyst_routes.analyst_dashboard'))


@bp.route('/api/incidents')
def api_get_incidents():
    from controllers.analyst import get_all_incidents
    incidents = get_all_incidents()
    return jsonify(incidents)

    return redirect(url_for('analyst_routes.analyst_dashboard'))


