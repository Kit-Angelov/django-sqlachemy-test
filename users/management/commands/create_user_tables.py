from django.core.management.base import BaseCommand, CommandError
from users import models
from django_alchemy.db_engine import engine


class Command(BaseCommand):

    def handle(self, *args, **options):
        models.Base.metadata.create_all(engine)
