# routes/__init__.py
from .auth_routes import bp as auth_routes_bp
from .admin_routes import bp as admin_routes_bp
from .analyst_routes import bp as analyst_routes_bp

def init_routes(app):
    app.register_blueprint(auth_routes_bp)
    app.register_blueprint(admin_routes_bp)
    app.register_blueprint(analyst_routes_bp)
