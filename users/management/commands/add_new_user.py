from django.core.management.base import BaseCommand, CommandError
from users import models
from django_alchemy.db_engine import DBSession
import datetime


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)
        parser.add_argument('first_name', type=str)
        parser.add_argument('second_name', type=str)
        parser.add_argument('patronymic', type=str)
        parser.add_argument('date_of_birth', type=str, help='format Y-m-d')
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        db_session = DBSession()
        date_of_birth = datetime.datetime.strptime(options['date_of_birth'], '%Y-%m-%d').date()
        user = models.User(email=options['email'],
                           first_name=options['first_name'],
                           second_name=options['second_name'],
                           patronymic=options['patronymic'],
                           date_of_birth=date_of_birth)
        user.set_password(options['password'])
        db_session.add(user)
        db_session.commit()