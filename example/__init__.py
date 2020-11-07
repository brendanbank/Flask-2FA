import ssc.config
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('ssc.config')

    from ssc.models import db
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    app.test = True

    from .views import register_blueprints
    register_blueprints(app)
                    
    return app
