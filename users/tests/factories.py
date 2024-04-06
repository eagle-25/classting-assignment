import factory

from users.models import Users


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Users

    email = factory.Faker("email")
    password = factory.Faker("password")
