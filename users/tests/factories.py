import factory

from users.adapter.outcome.persistence.models import Users


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Users

    email = factory.Faker("email")
    password = factory.Faker("password")
