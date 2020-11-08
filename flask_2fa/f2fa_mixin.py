import logging
log = logging.getLogger(__name__)
import time

""" mixin object to add to flask_login User Object to store and retrieve authenticator data """

class F2faUserMixin(object):
    """ get list of authenticator credentials """
    def get_2fa_cred(self):
        return self.credentials
    
    def get_credential(self,credential):
        log.debug(f'check if user {self.email} has {credential}')
        for cred in self.get_2fa_cred():
            if cred.credential_id == credential:
                log.debug(f'user {self.email} has {credential}')
                return True
        return(False)
    
    def has_f2fa_credentials(self):
        if self.get_2fa_cred():
            return True
        else:
            return False
            
class F2faChallangeMixin(object):

    @classmethod
    def set_challange(cls,request):
        return cls(request=request, timestamp_ms=int(time.time() * 1000))
        
    @classmethod
    def get_challange(cls,request):
        return cls.query.filter(cls.request==request).first()

class F2faCredentialMixin(object):
    @classmethod
    def update_signature_count(cls,credential_id,counter):
        credential = cls.query.filter(cls.credential_id==credential_id).first()
        credential.signature_count = counter;
        return(credential)
    
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


