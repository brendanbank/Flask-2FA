from flask import Blueprint, current_app, render_template_string, session
from flask_user import login_required
from flask_2fa.decorators import login_required_f2fa


public_blueprint = Blueprint('public', __name__, template_folder='templates')


@public_blueprint.route('/')
def home_page():
    return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>{%trans%}Home page{%endtrans%}</h2>
                <p><a href={{ url_for('user.register') }}>{%trans%}Register{%endtrans%}</a></p>
                <p><a href={{ url_for('user.login') }}>{%trans%}Sign in{%endtrans%}</a></p>
                <p><a href={{ url_for('public.home_page') }}>{%trans%}Home Page{%endtrans%}</a> (accessible to anyone)</p>
                <p><a href={{ url_for('admin_site.f2fa_credentials') }}>{%trans%}Credentials{%endtrans%}</a></p>
                <p><a href={{ url_for('user.logout') }}>{%trans%}Sign out{%endtrans%}</a></p>
                <p><a href={{ url_for('flask_2fa.register_token') }}>{%trans%}Register Token{%endtrans%}</a></p>
                <p><a href={{ url_for('flask_2fa.authenticate_token') }}>{%trans%}Authenticate Token{%endtrans%}</a></p>
                                
            {% endblock %}
            """)
    
@public_blueprint.route('/config')
@login_required
@login_required_f2fa
def config_items():
    session.pop('_f2fa_id')

    content = ""
    for k,v in current_app.config.items():
        content = content + f"<br>{k}={v}\n"
    
    return content
