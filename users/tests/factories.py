import factory
from faker import Faker

from users.models import Users

_fake = Faker()


class UsersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Users

    email = _fake.email()
    name = factory.Faker("name")
    password = factory.Faker("password")
