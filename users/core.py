from .models import User, AuthToken
from django_alchemy.db_engine import DBSession
import datetime


def login(email, password):
    db_session = DBSession()
    password_hash_hexdigest = User.get_hash_password(password)
    user = db_session.query(User).filter_by(email=email, password=password_hash_hexdigest).first()
    if user:
        auth_token = user.auth_token
        if not auth_token:
            auth_token = AuthToken(user=user)
            db_session.add(auth_token)
        auth_token.update_access_and_refresh_tokens()
        db_session.commit()
    return user


def logout(access_token):
    db_session = DBSession()
    auth_token = db_session.query(AuthToken).filter_by(access_token=access_token).first()
    if auth_token:
        auth_token.delete_access_and_refresh_tokens()
        db_session.commit()


def authorize(access_token):
    db_session = DBSession()
    auth_token = db_session.query(AuthToken).filter_by(access_token=access_token).first()
    if auth_token:
        datetime_now = datetime.datetime.now()
        if datetime_now < auth_token.access_token_expiration_date:
            return auth_token.user
