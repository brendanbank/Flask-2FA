from flask import Blueprint

public_blueprint = Blueprint('public', __name__, template_folder='templates')


@public_blueprint.route('/')
def home():
    return('Hello World!')