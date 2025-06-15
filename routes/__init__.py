# routes/__init__.py
def init_routes(app):
    from . import auth_routes, admin_routes, analyst_routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(admin_routes.bp)
    app.register_blueprint(analyst_routes.bp)
