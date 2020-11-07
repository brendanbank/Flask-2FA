import six
from enum import Enum, unique
import fido2

class _StringEnum(six.text_type, Enum):
    @classmethod
    def _wrap(cls, value):
        if value is None:
#             return None
            return cls('None')
        return cls(value)
@unique
class AuthenitcatorTokenType(_StringEnum):
    PLATFORM = "platform"
    CROSS_PLATFORM = "cross-platform"
    ANY = None



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
    