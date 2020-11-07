import logging
log = logging.getLogger(__name__)
import time

""" mixin object to add to flask_login User Object to store and retrieve authenticator data """

class F2faMixin(object):
    """ get list of authenticator credentials """
    def get_2fa_cred(self):
        log.debug(f'credentials: {self.credentials}')
        return []
        
    """ add an authenticator credential to the user credentials table """
    def add_2fa_cred(self):
        return True

    def delete_2fa_cred(self):
        return True

class F2faCredentialMixin(object):

        @classmethod
        def set_challange(cls,request):
            self = cls()
            self.request = request
            self.timestamp_ms = int(time.time() * 1000)
            return(self)
            

