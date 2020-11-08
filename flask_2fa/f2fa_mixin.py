import logging
from ipaddress import ip_address
log = logging.getLogger(__name__)
import time

""" mixin object to add to flask_login User Object to store and retrieve authenticator data """

class F2faUserMixin(object):
    """ get list of authenticator credentials """
    def get_2fa_cred(self):
        log.debug(f'credentials: {self.credentials}')
        return self.credentials
            
class F2faChallangeMixin(object):

    @classmethod
    def set_challange(cls,request):
        return cls(request=request, timestamp_ms=int(time.time() * 1000))
        
    @classmethod
    def get_challange(cls,request):
        return cls.query.filter(cls.request==request).first()

class F2faCredentialMixin(object):
    @classmethod
    def add_credential(cls,credential,credential_id, request):

        ip_address = request.remote_addr
        user_agent = request.user_agent
                
        instance  = cls(
            credential=credential, 
            credential_id=credential_id,
            ip_address=ip_address,
            user_agent=user_agent,
            )
        
        return instance


