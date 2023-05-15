from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = "Create super user"

    def handle(self, *args, **options):
        data = {
            "username": "admin100",
            "password": "12345678",
            "is_staff": True,
            "is_active": True,
        }
        created_user = apps.get_model(
            "beta_user.BetaUser",
        ).objects.create(**data)

        if created_user:
            print("Super user is created.")

