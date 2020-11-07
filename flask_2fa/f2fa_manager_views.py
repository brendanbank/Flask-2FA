from flask_user import login_required, current_app, current_user
from flask import render_template
from flask import session, abort
from fido2 import cbor 
import logging
log = logging.getLogger(__name__)


class F2faManager__Views(object):
    
    @login_required
    def register_token_view(self):
        # Render form
        return render_template(self.F2FA_REGISTER_TOKEN_VIEW)
    
    @login_required
    def submit_token_view(self):
        return render_template(self.F2FA_SUBMIT_TOKEN_VIEW)

    @login_required
    def api_register_begin(self):
        
        server = current_app.flask_2fa.reply_party_server.server
        if not current_user:
            return abort(404)
                
        print(self.F2FA_AUTHENTICATOR_TOKEN.value if self.F2FA_AUTHENTICATOR_TOKEN else None)
        
        registration_data, state = server.register_begin(
            {
                "id": bytes(str(current_user.id).encode('utf8')),
                "name": current_user.email,
                "displayName": f'{current_user.first_name} {current_user.last_name}',
                "icon": "https://example.com/image.png",
            },
            current_user.get_2fa_cred(),
            user_verification=self.F2FA_USER_VERIVICATION.value if self.F2FA_USER_VERIVICATION else None,
            authenticator_attachment= None,
        )
        
        challance = self.challange_cls.set_challange(state['challenge'])
        
        current_user.challenges.append(challance)
        self.db.session.commit()
        
        
        session["state"] = state
        print("\n\n\n\n")
        print(registration_data)
        print('state', state)
        print("\n\n\n\n")
        return cbor.encode(registration_data)

    @login_required
    def api_register_complete(self):
        pass
