import os, sys
from flask import Flask
from routes import init_routes

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from db.db_config import get_connection
from db.model import create_tables

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

# Create required tables on startup
conn = get_connection()
create_tables(conn)
conn.close()

# Register all routes
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
