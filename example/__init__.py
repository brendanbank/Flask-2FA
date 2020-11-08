from flask_user import UserManager
from flask_2fa import F2faManager
from flask_wtf.csrf import CSRFProtect


from flask import Flask
import flask_2fa


def create_app():
    app = Flask(__name__)
    app.config.from_object('example.config')
    
    csrf_protect = CSRFProtect()
    csrf_protect.init_app(app)
    
    from .models import db
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    app.test = True

    from .views import register_blueprints
    register_blueprints(app)
    from .models.users import User, Challenge, Credential
    
    user_manager = UserManager(app, db, User)
    f2fa_manager = F2faManager(app, db, User, Credential, Challenge)

    @app.context_processor
    def context_processor_user_manager():
        return dict(user_manager=user_manager)
    
    @app.context_processor
    def context_processor_flask_2fa():
        return dict(f2fa_manager=f2fa_manager)

    app.flask_2fa = flask_2fa
    return app
