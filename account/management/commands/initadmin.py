from faker import Faker
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        if not User.objects.filter(username=options['username']).exists() and not User.objects.filter(email=options['email']).exists():
            username = options['username']
            email = options['email']
            password = options['password']
            print('Creating account for %s (%s)' % (username, email))
            admin = User.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.is_staff = True
            admin.save()
        else:
            print('Admin accounts with these credentials exist')