from functools import wraps
from flask import current_app, g, session
from flask_login import current_user
import time


def _is_logged_in_with_token(f2fa_manager):
    
    if ('_f2fa_expire' in session 
            and '_f2fa_id' in session 
            and session['_f2fa_expire'] > time.time() 
            and current_user.get_credential( session['_f2fa_id'] )
            ):
        return True    
    
    return(False)

def login_required_f2fa(view_function):
    
    @wraps(view_function)    # Tells debuggers that is is a function wrapper
    def decorator(*args, **kwargs):
        f2fa_manager = current_app.f2fa_manager
        
        # User must be logged in with a confirmed email address
        allowed = _is_logged_in_with_token(f2fa_manager)
        if not allowed:
            # Redirect to unauthenticated page
            return f2fa_manager.unauthenticated_token_view()

        # It's OK to call the view
        return view_function(*args, **kwargs)

    return decorator
