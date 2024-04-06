import logging

import factory

from users.models import Users

logger = logging.getLogger(__name__)


class UsersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Users

    email = factory.Faker("email")
    password = factory.Faker("password")
