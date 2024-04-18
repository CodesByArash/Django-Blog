from faker import Faker
from account.models import User
from core.models import Post
from django.shortcuts import get_object_or_404
from django.core.management.base import BaseCommand




class Command(BaseCommand):
    help = 'this command generates fake data for user model'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int)

    def handle(self,*args, **kwargs):
        number = kwargs .get("number")
        faker  = Faker()
        for _ in range(number):
            while True:
                username   = faker.user_name()
                email      = faker.email()
                user       = User.objects.filter(username=username).first()
                user2      = User.objects.filter(email=email).first()
                if (user is None) and (user2 is None):
                    break
            first_name = faker.first_name()
            last_name  = faker.last_name()
            bio        = faker.paragraph(nb_sentences=2)
            user = User.objects.create(username=username,email=email,
                    first_name=first_name,last_name=last_name,bio=bio)



        print("fake users generated")

 