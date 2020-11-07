from .admin import admin_blueprint
from .public import public_blueprint

def register_blueprints(app):
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(public_blueprint)
