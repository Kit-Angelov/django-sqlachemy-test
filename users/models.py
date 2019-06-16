import hashlib
import uuid
import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DATE
from sqlalchemy.orm import relationship
from django.conf import settings


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255))
    second_name = Column(String(255))
    patronymic = Column(String(255))
    date_of_birth = Column(DATE)
    email = Column(String(255))
    password = Column(String(255))
    auth_token = relationship("AuthToken", uselist=False, back_populates="user")
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship("City", back_populates="user")

    def __repr__(self):
        return "<User(first_name='%s', second_name='%s', email='%s')>" % (
            self.first_name, self.second_name, self.email)

    @classmethod
    def get_hash_password(cls, password):
        password_src = password + settings.SECRET_KEY
        password_hash = hashlib.md5(password_src.encode())
        password_hash_hexdigest = password_hash.hexdigest()
        return password_hash_hexdigest

    def set_password(self, password):
        password_hash_hexdigest = User.get_hash_password(password)
        self.password = password_hash_hexdigest


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    user = relationship("User", back_populates="city")


class AuthToken(Base):
    __tablename__ = 'auth_token'

    id = Column(Integer, primary_key=True, autoincrement=True)
    access_token = Column(String(255), nullable=True)
    access_token_expiration_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="auth_token")

    def __repr__(self):
        return "<AuthToken(user_id='%s', access_token='%s')>" % (
            self.user_id, self.access_token)

    # создание нового токена и расчет его время жизни
    def create_access_token(self):
        access_token = str(uuid.uuid4())
        self.access_token = access_token

        access_token_exiparation_data = datetime.datetime.now() + relativedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRATION_DELTA_MINUTES)
        self.access_token_expiration_date = access_token_exiparation_data

    # верификация токена (проверка на совпадение и по времени жизни)
    def verify_access_token(self):
        datetime_now = datetime.datetime.now()
        if datetime_now < self.access_token_expiration_date:
            return True
        else:
            return False

    # удаление токена
    def delete_access_tokens(self):
        self.access_token = None

