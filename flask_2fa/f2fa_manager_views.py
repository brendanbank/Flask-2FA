from flask_user import login_required, current_app, current_user
from flask import render_template
from flask import session, abort, url_for, flash, redirect
from fido2 import cbor 
from flask import request
import logging
log = logging.getLogger(__name__)

from fido2.utils import websafe_encode
from fido2.client import ClientData
from fido2.ctap2 import AttestationObject, AuthenticatorData
import time
from urllib.parse import quote, unquote

class F2faManager__Views(object):
    
    @login_required
    def register_token_view(self):
        # Render             
        safe_next_url = self._get_safe_next_url('next', self.F2FA_AFTER_REGISTER)
        return render_template(self.F2FA_REGISTER_TOKEN_VIEW,next=safe_next_url)

    @login_required
    def unauthenticated_token_view(self):
        """ Prepare a Flash message and redirect to UF2FA_UNAUTHENTICATED_ENDPOINT"""
        # Prepare Flash message
        url = request.url
        safe_next_url = self.make_safe_url(url)
        
        """ check if the user has 2fa credential """
        if (not current_user.has_f2fa_credentials()):
            """ redirect to f2fa registration endpoint """
            flash(f"You have a 2fa token to access '{url}'. Please create one", 'error')

            return redirect(self._endpoint_url(self.UF2FA_REGISTRATION_ENDPOINT)+'?next='+quote(safe_next_url))
        
        flash(f"You must be signed in with an 2fa token to access '{url}'.", 'error')

        # Redirect to UF2FA_UNAUTHENTICATED_ENDPOINT
        return redirect(self._endpoint_url(self.UF2FA_UNAUTHENTICATED_ENDPOINT)+'?next='+quote(safe_next_url))
    
    @login_required
    def authenticate_token_view(self):

        safe_next_url = self._get_safe_next_url('next', self.F2FA_AFTER_AUTHENTICATION)
        return render_template(self.F2FA_AUTHENTICATE_TOKEN_VIEW, next=safe_next_url)

    @login_required
    def api_authenticate_begin(self):
        credentials = self.fido2_credentials(current_user.get_2fa_cred())
        if not credentials:
            abort(404)
            
        server = current_app.f2fa_manager.reply_party_server.server
        auth_data, state = server.authenticate_begin(credentials)
        session["state"] = state
        return cbor.encode(auth_data)

    @login_required
    def api_authenticate_complete(self):
        credentials = self.fido2_credentials(current_user.get_2fa_cred())
        if not credentials:
            abort(404)

        data = cbor.decode(request.get_data())
        credential_id = data["credentialId"]
        client_data = ClientData(data["clientDataJSON"])
        auth_data = AuthenticatorData(data["authenticatorData"])
        signature = data["signature"]

        server = current_app.f2fa_manager.reply_party_server.server
        cred = server.authenticate_complete(
            session.pop("state"),
            credentials,
            credential_id,
            client_data,
            auth_data,
            signature,
        )
        
        credential_id = websafe_encode(cred.credential_id)
        
        log.info(f'user {current_user.email} logged into with credentials {credential_id}.')
        
        """ Token authentication succeeded. Set session vars to reflect this """
        
        self.f2fa_login(credential_id)
                
        return cbor.encode({"status": "ok"})
    
    @login_required
    def api_register_begin(self):
        
        if not current_user:
            return abort(404)


        credentials = self.fido2_credentials(current_user.get_2fa_cred())
        server = current_app.f2fa_manager.reply_party_server.server
        registration_data, state = server.register_begin(
            {
                "id": bytes(str(current_user.id).encode('utf8')),
                "name": current_user.email,
                "displayName": f'{current_user.first_name} {current_user.last_name}',
                "icon": "https://example.com/image.png",
            },
            credentials,
#             current_user.get_2fa_cred(),
            user_verification=self.F2FA_USER_VERIVICATION.value if self.F2FA_USER_VERIVICATION else None,
            authenticator_attachment= self.F2FA_AUTHENTICATOR_TOKEN.value if self.F2FA_AUTHENTICATOR_TOKEN else None,
        )
        
        challance = self.challange_cls.set_challange(state.get('challenge'))
        log.debug(f"set_challange: {state.get('challenge')}")
        bin_challange = registration_data['publicKey']['challenge']
        
        log.debug(f"registration_data.publicKey.challenge {websafe_encode(bin_challange)}")
        current_user.challenges.append(challance)
        
        self.db.session.commit()
        
        session["state"] = state
        return cbor.encode(registration_data)

    @login_required
    def api_register_complete(self):
        
        data = cbor.decode(request.get_data())
        client_data = ClientData(data["clientDataJSON"])
        att_obj = AttestationObject(data["attestationObject"])
        server = current_app.f2fa_manager.reply_party_server.server
        auth_data = server.register_complete(session["state"], client_data, att_obj)
        
        challange_stored = self.challange_cls.get_challange(websafe_encode(client_data.challenge))
        
        if (challange_stored):
            self.db.session.delete(challange_stored)
            self.db.session.commit()
            if ((int(time.time() * 1000) > (challange_stored.timestamp_ms + self.F2FA_CHALLANGE_TIMEOUT))):
                log.error(f'challange expired for user {current_user.email}')
                return cbor.encode({"status": "Challenge Expired!"})
            

        else:
            log.error(f'Request with no challenge?? {current_user.email}')

            log.debug(f'challange {challange_stored} does not exists or is invalid')
            return cbor.encode({"status": "Challenge does not exists!"})
        
        crediential_id = websafe_encode(auth_data.credential_data.credential_id)
        crediential_encoded = websafe_encode(auth_data.credential_data)
        
        log.debug(f'credential_id {crediential_id}')
        log.debug(f'credential_data {crediential_encoded}')
        
        credential_dbinstance = self.credential_cls.add_credential(crediential_encoded,crediential_id,request)
        
        current_user.credentials.append(credential_dbinstance)
        
        self.db.session.commit()
        
        return cbor.encode({"status": "ok"})

    # Returns safe URL from query param ``param_name`` if query param exists.
    # Returns url_for(default_endpoint) otherwise.
    
    def _get_safe_next_url(self, param_name, default_endpoint):

        # Returns safe URL from query param ``param_name`` if query param exists.
        if param_name in request.args:
            safe_next_url = current_app.user_manager.make_safe_url(unquote(request.args[param_name]))

        # Returns url_for(default_endpoint) otherwise.
        else:
            safe_next_url = self._endpoint_url(default_endpoint)

        return safe_next_url


    def _endpoint_url(self, endpoint):
        return url_for(endpoint) if endpoint else '/'

