from flask import Blueprint, render_template, redirect, url_for, abort
from flask_user import login_required, current_user
from flask_2fa import login_required_f2fa
import user_agents 

from ..models import db

from ..models import CredentialForm
from ..models.users import Credential

admin_blueprint = Blueprint('admin_site', __name__, template_folder='templates')


@admin_blueprint.route('/admin/2fa/credentials')
@login_required
@login_required_f2fa
def f2fa_credentials():
    credentials = current_user.get_2fa_cred()
    creds = []
    for credential in credentials:
        
        ua = user_agents.parse(credential.user_agent)
        user_string = f'{ua.device.brand}/{ua.device.model}-{ua.os.family} ({ua.os.version_string})'
        user_string = f'{ua.device.brand} {ua.device.model} / {ua.os.family} ({ua.os.version_string}) {ua.browser.family} ({ua.browser.version_string})'
        print (user_string)
        creds.append({'form': CredentialForm(obj=credential),
                      'obj': credential,
                      'user_agent': user_string
                      })
        
    
    return render_template('admin/credentials.html',credentials=creds)



@admin_blueprint.route('/admin/2fa/credential/<int:id>/<action>', methods=['POST','GET'])
@login_required
@login_required_f2fa
def f2fa_credential(id=None,action=None ):

    credential = db.session.query(Credential).filter(Credential.user_id == current_user.id, 
                                                     Credential.id==id).first()
    if not credential:
        return abort(404)
    
    if action == 'delete':
        db.session.delete(credential)
        db.session.commit()
        return redirect(url_for('admin_site.f2fa_credentials'))
        
    form = CredentialForm(obj=credential)
    if form.validate_on_submit():
        form.populate_obj(credential)
        db.session.commit()

    return redirect(url_for('admin_site.f2fa_credentials'))

