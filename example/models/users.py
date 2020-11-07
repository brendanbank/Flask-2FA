from flask_user import UserMixin
from flask_2fa import F2faMixin
from . import db



# Define the User data model. Make sure to add the flask_user.UserMixin !!

class User(db.Model, UserMixin, F2faMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    # reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')

    # Relationships
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('user', lazy='dynamic'))


    credentials = db.relationship('Credential',
                                  backref=db.backref('user', lazy=True))
    challenges = db.relationship('Challenge',
                                 backref=db.backref('user', lazy=True))

# Define the Role data model
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes


# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

class Credential(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    signature_count = db.Column(db.Integer, nullable=True)
    credential = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request = db.Column(db.String(255), unique=True)
    timestamp_ms = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)