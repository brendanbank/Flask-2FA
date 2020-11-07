
from .f2fa_manager_settings import F2faManager__Settings
from .f2fa_manager_utils import F2faManager__Utils
from .f2fa_manager_views import F2faManager__Views



from flask import Flask, Blueprint

import six
from enum import Enum, unique


from . import ConfigError
from . import forms

import logging
log = logging.getLogger(__name__)

from .replying_party_server import ReplyingPartyServer


# classes to ensure validity of the configuration items.

class _StringEnum(six.text_type, Enum):
    @classmethod
    def _wrap(cls, value):
        if value is None:
            return None
        return cls(value)
@unique
class AuthenitcatorTokenType(_StringEnum):
    PLATFORM = "platform"
    CROSS_PLATFORM = "cross-platform"

@unique
class UserVerificationRequirementType(_StringEnum):
    REQUIRED = "required"
    PREFERRED = "preferred"
    DISCOURAGED = "discouraged"



class F2faManager(F2faManager__Settings, F2faManager__Utils, F2faManager__Views):
    def __init__(self, app, db, UserClass, CredintialClass, ChallangeClass, **kwargs):
        """
        Args:
            app(Flask): The Flask application instance.
            db: An Object-Database Mapper instance such as SQLAlchemy or MongoEngine.
            UserClass: The User class (*not* an instance!).
        """
        log.debug(f'started')
        self.app = app
        
        if app:
            
            self.init_app(app, db, UserClass, CredintialClass, ChallangeClass, **kwargs)

    def init_app(
        self, app, db, UserClass, CredintialClass, ChallangeClass):
        log.debug(f'started')

        # See http://flask.pocoo.org/docs/0.12/extensiondev/#the-extension-code
        # Perform Class type checking
        if not isinstance(app, Flask):
            raise TypeError("flask_user.UserManager.init_app(): Parameter 'app' is an instance of class '%s' "
                            "instead of a subclass of class 'flask.Flask'."
                            % app.__class__.__name__)

        self.user_cls = UserClass
        self.credential_cls = CredintialClass
        self.challange_cls = ChallangeClass


        # Bind Flask-2FA to app
        app.f2fa_manager = self
        self.db = db
        
        
        # Load app config settings
        # ------------------------
        # For each 'UserManager.USER_...' property: load settings from the app config.
        for attrib_name in dir(self):
            if attrib_name[0:5] == 'F2FA_':
                default_value = getattr(F2faManager, attrib_name)
                setattr(self, attrib_name, app.config.get(attrib_name, default_value))
                log.debug(f'set configuration {attrib_name} to {getattr(self, attrib_name)}')
                
                
        # Configure Flask-BabelEx
        # -----------------------
        self.babel = app.extensions.get('babel', None)
        from .translation_utils import init_translations
        init_translations(self.babel)

        # Configure Jinja2
        # ----------------
        # If the application has not initialized BabelEx,
        # we must provide a NULL translation to Jinja2
        if not hasattr(app.jinja_env, 'install_gettext_callables'):
            app.jinja_env.add_extension('jinja2.ext.i18n')
            app.jinja_env.install_null_translations()


        # Create a dummy Blueprint to add the app/templates/flask_user dir to the template search path
        blueprint = Blueprint('flask_2fa', __name__, url_prefix="/f2fa", static_folder='static', template_folder='templates')
        
        app.register_blueprint(blueprint)
        
        
        # Set default form classes
        # ------------------------
        self.ListCredentials = forms.ListCredentials
        
        # Setup reply part server
        self.reply_party_server = ReplyingPartyServer(app)
        
        self._check_settings(app)
        
        self._add_url_routes(app)
        

    def _add_url_routes(self, app):
        """Configure a list of URLs to route to their corresponding view method.."""

        # Because methods contain an extra ``self`` parameter, URL routes are mapped
        # to stub functions, which simply call the corresponding method.

        # For testing purposes, we map all available URLs to stubs, but the stubs
        # contain config checks to return 404 when a feature is disabled.

        # Define the stubs
        # ----------------

        def register_token_stub():
            return self.register_token_view()

        def submit_token_stub():
            return self.submit_token_view()
        
        def api_register_begin_sub():
            return self.api_register_begin()
        
        def api_register_complete_sub():
            return self.api_register_complete()
        

        app.add_url_rule(self.F2FA_API_REGISTER_COMPLETE_URL, 'flask_2fa.api_register_complete', api_register_complete_sub,
                         methods=['GET', 'POST'])

        app.add_url_rule(self.F2FA_API_REGISTER_BEGIN_URL, 'flask_2fa.api_register_begin', api_register_begin_sub,
                         methods=['GET', 'POST'])

        app.add_url_rule(self.F2FA_SUBMIT_TOKEN_URL, 'flask_2fa.submit_token', submit_token_stub,
                         methods=['GET', 'POST'])

        app.add_url_rule(self.F2FA_REGISTER_TOKEN_URL, 'flask_2fa.register_token', register_token_stub,
                 methods=['GET', 'POST'])


    def _check_settings(self, app):
        """Verify required settings. Produce a helpful error messages for incorrect settings."""

        # Check for invalid settings

        try:
            self.F2FA_AUTHENTICATOR_TOKEN=AuthenitcatorTokenType._wrap(
                self.F2FA_AUTHENTICATOR_TOKEN
                )
        except:
            options = '"' + '", "'.join(AuthenitcatorTokenType.__members__.values()) + '"'
            raise ConfigError(f'F2FA_AUTHENTICATOR_TOKEN is currently set to {self.F2FA_AUTHENTICATOR_TOKEN} '
                              f'F2FA_AUTHENTICATOR_TOKEN can only contain options: {options}, and None. '
                              'For more information on these settings check out:'
                              'https://developers.yubico.com/WebAuthn/WebAuthn_Developer_Guide/Platform_vs_Cross-Platform.html')


        try:
            self.F2FA_USER_VERIVICATION=UserVerificationRequirementType._wrap(
                self.F2FA_USER_VERIVICATION
                )
        except:
            options = '"' + '", "'.join(UserVerificationRequirementType.__members__.values()) + '"'
            raise ConfigError(f'F2FA_USER_VERIVICATION is currently set to {self.F2FA_USER_VERIVICATION} '
                              f'F2FA_USER_VERIVICATION can only contain options: {options}, and None. '
                              'For more information on these settings check out:'
                              'https://developers.yubico.com/WebAuthn/WebAuthn_Developer_Guide/User_Presence_vs_User_Verification.html')
