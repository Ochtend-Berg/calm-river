# ------------------------------------------------------------------------------------------------------------------------------------------ #

from app import app, db, login_manager
from imports import *


# ------------------------------------------------------------------------------------------------------------------------------------------ #

class User(db.Model, UserMixin):
    # -- TABLE NAME -- #
    __tablename__ = 'users'

    # -- TABLE COLUMNS -- #
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    is_admin = db.Column(db.Integer(), index=True, default=0)
    password_hash = db.Column(db.String(128))

    # -- CONSTRUCTOR -- #
    def __init__(self, email, username, is_admin, password):
        self.email = email
        self.username = username
        self.is_admin = 0
        self.password_hash = generate_password_hash(password)

    # -- CHECKS PASSWORD USER -- #
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # -- GETS CURRENT LOGIN-IN USER ID -- #
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    def generate_password_reset_token(self):
        token = serializer.dumps(self.email, salt='password-reset')
        return token

    @staticmethod
    def verify_password_reset_token(token):
        try:
            email = serializer.loads(token, salt='password-reset', max_age=3600)
            return User.query.filter_by(email=email).first()
        except:
            return None

# ------------------------------------------------------------------------------------------------------------------------------------------ #
