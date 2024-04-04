import factory
from faker import Faker

from users.models import Users


class UsersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Users

    fake = Faker()

    email = fake.email()
    name = factory.Faker("name")
    password = factory.Faker("password")
