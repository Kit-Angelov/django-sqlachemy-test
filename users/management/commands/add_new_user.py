from django.core.management.base import BaseCommand, CommandError
from users import models
from django_alchemy.db_engine import engine


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)
        parser.add_argument('first_name', type=str)
        parser.add_argument('second_name', type=str)
        parser.add_argument('patronymic', type=str)
        parser.add_argument('date_of_birth', type=str)
        parser.add_argument('password', type=str)


    def handle(self, *args, **options):
        pass