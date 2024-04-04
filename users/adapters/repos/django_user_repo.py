from django.db import IntegrityError

from users.domain.entities import UserEntity
from users.domain.exceptions import UserCreateFailed, UserNotFound
from users.domain.interfaces import IUserRepo
from users.models import Users


class DjangoOrmUserRepo(IUserRepo):
    def get(self, email: str, password: str) -> UserEntity:
        try:
            return Users.objects.get(email=email, password=password).to_entity()
        except Users.DoesNotExist:
            raise UserNotFound

    def create(self, entity: UserEntity):
        try:
            Users.from_entity(entity).save()
        except IntegrityError:
            raise UserCreateFailed
