from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        username = config('SUPERUSER_USERNAME')
        email = config('SUPERUSER_EMAIL')
        password = config('SUPERUSER_PASSWORD')  # Set a default password here

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser name:{username} created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser name:{username} already exists'))
