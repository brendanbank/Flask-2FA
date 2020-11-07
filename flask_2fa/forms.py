from flask import current_app
from flask_login import current_user

from flask_wtf import FlaskForm
from wtforms import BooleanField, HiddenField, PasswordField, SubmitField, StringField
from wtforms import validators, ValidationError

from .translation_utils import lazy_gettext as _    # map _() to lazy_gettext()


# ***********
# ** Forms **
# ***********

class ListCredentials(FlaskForm):
    pass
