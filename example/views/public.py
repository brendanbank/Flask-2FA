from flask import Blueprint, current_app

public_blueprint = Blueprint('public', __name__, template_folder='templates')


@public_blueprint.route('/')
def home():
    return('Hello World!')

@public_blueprint.route('/config')
def config_items():
    content = ""
    for k,v in current_app.config.items():
        content = content + f"<br>{k}={v}\n"
    
    return content
