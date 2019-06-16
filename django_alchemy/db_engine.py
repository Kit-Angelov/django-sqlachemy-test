from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


# провека на существование базы (в противном случае создание базы)
if not database_exists(settings.DATABASE_URI):
    create_database(settings.DATABASE_URI)

# подключение к бд
engine = create_engine(settings.DATABASE_URI, echo=True)

# клиент сессии подключения к бд
DBSession = sessionmaker()
DBSession.configure(bind=engine)

