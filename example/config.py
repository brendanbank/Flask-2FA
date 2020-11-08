import logging, sys
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

FLASK_ENV = os.getenv("FLASK_ENV", 'production')

if (FLASK_ENV=="development"):
    logging.basicConfig(format='%(asctime)s %(name)s.%(funcName)s(%(lineno)s): %(message)s',stream=sys.stderr,level=logging.DEBUG)
    SQLALCHEMY_ECHO=False
else:
    logging.basicConfig(format='%(asctime)s %(name)s.%(funcName)s(%(lineno)s): %(message)s',stream=sys.stderr,level=logging.INFO)
    SQLALCHEMY_ECHO=False

    
log = logging.getLogger(__name__)
log.debug(f'started')

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Flask-Mail settings
# For smtp.gmail.com to work, you MUST set "Allow less secure apps" to ON in Google Accounts.
# Change it in https://myaccount.google.com/security#connectedapps (near the bottom).
MAIL_SERVER = '10.0.20.2'
MAIL_PORT = 25
MAIL_USE_SSL = False
MAIL_USE_TLS = False
MAIL_USERNAME = None
MAIL_PASSWORD = None

# Flask-User settings
USER_APP_NAME = 'Flask-User starter app'
USER_EMAIL_SENDER_NAME = 'Brendan Bank'
USER_EMAIL_SENDER_EMAIL = 'brendan.bank@gmail.com'
MAIL_DEFAULT_SENDER = USER_EMAIL_SENDER_EMAIL

# Flask settings
CSRF_ENABLED = True

# Flask-SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = '.kjasdhfkjashdfkljhsalkdfjhlkasjdhfkjasljw;oiuwe;jhaskj.kmnsavclkuhqegiuy7039874iulyhwdliuysdoy'

# Flask-User settings
USER_APP_NAME = 'Flask-F2fa demo app'
USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
USER_ENABLE_CHANGE_USERNAME = False  # Allow users to change their username
USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
USER_ENABLE_EMAIL = True  # Register with Email
USER_ENABLE_REGISTRATION = True  # Allow new users to register
USER_REQUIRE_RETYPE_PASSWORD = True  # Prompt for `retype password` in:
USER_ENABLE_USERNAME = False  # Register and Login with username
USER_AUTO_LOGIN_AFTER_RESET_PASSWORD = True
USER_ENABLE_REGISTER = True
USER_ENABLE_FORGOT_PASSWORD = True

USER_ENABLE_REMEMBER_ME = True

#REMEMBER_COOKIE_NAME='gira_remember_token'

F2FA_AUTHENTICATOR_TOKEN=None
F2FA_USER_VERIVICATION='discouraged'
# F2FA_AFTER_REGISTER = 'public.home_page'