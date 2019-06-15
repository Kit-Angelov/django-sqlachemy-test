from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


if not database_exists(settings.SQLALCHEMY_DATABASE_URI):
    create_database(settings.SQLALCHEMY_DATABASE_URI)

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)

DBSession = sessionmaker()
DBSession.configure(bind=engine)
