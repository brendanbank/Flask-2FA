
""" mixin object to add to flask_login User Object to store and retrieve authenticator data """

class F2faMixin(object):
    """ get list of authenticator credentials """
    def get_2fa_cred(self):
        return[]
        
    """ add an authenticator credential to the user credentials table """
    def add_2fa_cred(self):
        return True

    def delete_2fa_cred(self):
        return True
