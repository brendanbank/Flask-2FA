__title__       = 'Flask-2FA'
__description__ = 'Customizable 2FA Authentication, based on Flask-User and Flask-Login.'
__version__     = '0.0.1'
__url__         = 'https://github.com/lingthio/Flask-User'
__author__      = 'Brendan Bank'
__author_email__= 'brendan.bank@gmail.com'
__maintainer__  = 'Brendan Bank'
__license__     = 'MIT'
__copyright__   = '(c) 2020 Brendan Bank'


class ConfigError(Exception):
    pass

# Export Flask-Login's current user
from flask_login import current_user    # pass through Flask-Login's current_user


from .f2fa_mixin import F2faMixin
from .f2fa_manager import F2faManager



