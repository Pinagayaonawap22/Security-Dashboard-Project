import os, sys
from flask import Flask
from routes import init_routes

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from db.db_config import get_connection
from db.model import create_tables

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

try:
    conn = get_connection()
    create_tables(conn)
    conn.close()
except Exception as e:
    print(f"[ERROR] Failed to connect to database on startup: {e}")


# Register all routes
init_routes(app)

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

