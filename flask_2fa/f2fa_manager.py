
from .f2fa_manager_settings import F2faManager__Settings
from .f2fa_manager_utils import F2faManager__Utils
from .f2fa_manager_views import F2faManager__Views
from flask import Flask

import logging
log = logging.getLogger(__name__)

class F2faManager(F2faManager__Settings, F2faManager__Utils, F2faManager__Views):
    def __init__(self, app, db, UserClass, **kwargs):
        """
        Args:
            app(Flask): The Flask application instance.
            db: An Object-Database Mapper instance such as SQLAlchemy or MongoEngine.
            UserClass: The User class (*not* an instance!).
        """
        log.debug(f'started')
        self.app = app
        
        if app:
            
            self.init_app(app, db, UserClass, **kwargs)

    def init_app(
        self, app, db, UserClass):
        log.debug(f'started')

        # See http://flask.pocoo.org/docs/0.12/extensiondev/#the-extension-code
        # Perform Class type checking
        if not isinstance(app, Flask):
            raise TypeError("flask_user.UserManager.init_app(): Parameter 'app' is an instance of class '%s' "
                            "instead of a subclass of class 'flask.Flask'."
                            % app.__class__.__name__)

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
                log.debug(f'set configuration {getattr(self, attrib_name)}')
                
                
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


