from .models import User, AuthToken
from django_alchemy.db_engine import DBSession
import datetime


# аутентификация. Создается токен и задается время его жизни
def login(email, password):
    db_session = DBSession()
    password_hash_hexdigest = User.get_hash_password(password)
    user = db_session.query(User).filter_by(email=email, password=password_hash_hexdigest).first()
    if user:
        auth_token = user.auth_token
        if not auth_token:
            auth_token = AuthToken(user=user)
            db_session.add(auth_token)
        auth_token.create_access_token()
        db_session.commit()
    return user


# выход. Удаляется токен
def logout(user):
    db_session = DBSession.object_session(user)
    auth_token = user.auth_token
    if auth_token:
        auth_token.delete_access_tokens()
        db_session.commit()


# авторизация. Провека на существование и на время его жизни
def authorize(access_token):
    db_session = DBSession()
    auth_token = db_session.query(AuthToken).filter_by(access_token=access_token).first()
    if auth_token:
        if auth_token.verify_access_token():
            return auth_token.user


# обновление токена. Получение токена и (если он есть) создание нового
def refresh_token(access_token):
    db_session = DBSession()
    auth_token = db_session.query(AuthToken).filter_by(access_token=access_token).first()
    if auth_token:
        auth_token.create_access_token()
        db_session.commit()
        return auth_token.access_token

