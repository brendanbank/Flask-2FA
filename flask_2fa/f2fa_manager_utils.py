from fido2.utils import websafe_encode, websafe_decode
from fido2.ctap2 import AttestedCredentialData
from flask import session
import time, datetime
from urllib.parse import urlsplit, urlunsplit
import logging
log = logging.getLogger(__name__)

class F2faManager__Utils(object):


    def fido2_credentials(self,credentials):
        fido2_creds = []
        for cred in credentials:
            fido2_creds.append(AttestedCredentialData(websafe_decode(cred.credential)))
        return(fido2_creds)
    
    def f2fa_login(self,credential_id):
            
        """ add the credential_id to the session and if there is an expiration time set that too
        """
        expire_at = int(time.time()) + self.F2FA_CREDITNIAL_EXPIRATION
        session['_f2fa_expire'] = expire_at
        session['_f2fa_id'] = credential_id
        
        
    def make_safe_url(self, url):
        """Makes a URL safe by removing optional hostname and port.

        Example:

            | ``make_safe_url('https://hostname:80/path1/path2?q1=v1&q2=v2#fragment')``
            | returns ``'/path1/path2?q1=v1&q2=v2#fragment'``

        Override this method if you need to allow a list of safe hostnames.
        """

        # Split the URL into scheme, netloc, path, query and fragment
        parts = list(urlsplit(url))

        # Clear scheme and netloc and rebuild URL
        parts[0] = ''   # Empty scheme
        parts[1] = ''   # Empty netloc (hostname:port)
        safe_url = urlunsplit(parts)
        return safe_url
