from django.core.management.base import BaseCommand
from faker import Faker
import random

from accounts.models import User, Profile
from ...models import Task


class Command(BaseCommand):
    help = "Insert fake tasks"

    def __init__(self):
        super().__init__()  # Call BaseCommand's __init__
        self.fake = Faker()  # Initialize Faker once here

    def handle(self, *args, **options):

        # Create random user:
        user = User.objects.create_user(email=self.fake.email(), password="anvari@7768")
        profile = Profile.objects.get(user=user)
        print(profile)

        # Define profile for random user created:
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.text(max_nb_chars=200)
        profile.save()

        # Create 5 Tasks in database:
        for _ in range(5):
            Task.objects.create(
                author=profile,
                title=self.fake.paragraph(nb_sentences=1),
                status=random.choice([True, False]),
            )
