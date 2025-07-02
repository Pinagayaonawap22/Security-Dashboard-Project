# routes/auth_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from db.db_config import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText

bp = Blueprint('auth_routes', __name__)

@bp.route('/')
def home():
    return redirect(url_for('auth_routes.register'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        email = request.form.get('email')
        if not username or not password or not role or not email:
            return "All fields are required", 400

        hashed_pw = generate_password_hash(password)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return "Username already exists", 409
        cur.execute("INSERT INTO users (username, password_hash, role, email) VALUES (%s, %s, %s, %s)",
                    (username, hashed_pw, role, email))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('auth_routes.login'))

    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['username'] = user['username']
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect(url_for('admin_routes.admin_dashboard'))
            elif user['role'] == 'analyst':
                return redirect(url_for('analyst_routes.analyst_dashboard'))
            else:
                return "Unknown role", 403
        return "Invalid credentials", 401

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth_routes.login'))

@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    message = None
    if request.method == 'POST':
        email = request.form.get('email')

        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            # 🔐 Example reset link (you can generate a token or just display password reset for now)
            reset_link = f"http://127.0.0.1:5000/reset-password?email={email}"
            send_reset_email(email, reset_link)
            message = "Reset link sent to your email."
        else:
            message = "Email not found."

    return render_template('forgot_password.html', message=message)


def send_reset_email(to_email, reset_link):
    sender_email = "nawap.programmer@gmail.com"
    sender_password = "sjxn urav apjv hbrl"  # Use app password (not your main password)
    subject = "Password Reset Request"
    body = f"Click the link to reset your password:\n{reset_link}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
    except Exception as e:
        print("Email failed to send:", e)
        
@bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    email = request.args.get('email')  # Get email from URL param

    if request.method == 'POST':
        new_password = request.form.get('new_password')

        if not new_password or not email:
            return "Missing email or password", 400

        hashed_pw = generate_password_hash(new_password)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET password_hash = %s WHERE email = %s", (hashed_pw, email))
        conn.commit()
        cur.close()
        conn.close()

        return "Password successfully updated. You may now log in."

    return render_template('reset_password.html', email=email)
