

class F2faManager__Settings(object):
    
    # set to None to allow any tokens to be used
    # see https://developers.yubico.com/WebAuthn/WebAuthn_Developer_Guide/Platform_vs_Cross-Platform.html
    
    F2FA_AUTHENTICATOR_TOKEN = None
    F2FA_PK_CREDIENTIAL_ID = 'localhost'
    F2FA_PK_CREDIENTIAL_NAME = 'Demo Site'

    # allows for %(user_email)s %(username)s
    F2FA_USER_ICON  = "https://example.com/image.png"
    
    """ We assume that the user is already authenticated with a username and password via flask_login or flask_user """
    """ see https://developers.yubico.com/WebAuthn/WebAuthn_Developer_Guide/User_Presence_vs_User_Verification.html for more information """
    
    F2FA_USER_VERIVICATION = "discouraged"
    
    
    """ Templates URLS """
    
    F2FA_REGISTER_TOKEN_URL = '/register-token' #:
    F2FA_REGISTER_TOKEN_VIEW = '/flask_2fa/register_token.html'
    
    F2FA_SUBMIT_TOKEN_URL = '/f2fa/submit-token' #:
    F2FA_SUBMIT_TOKEN_VIEW = '/flask_2fa/submit_token.html'
    
    
    F2FA_API_REGISTER_BEGIN_URL = '/f2fa/api/register/begin' #:
    F2FA_API_REGISTER_COMPLETE_URL = '/f2fa/api/register/complete' #:

