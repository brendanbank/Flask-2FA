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

