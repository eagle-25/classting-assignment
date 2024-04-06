from django.db import IntegrityError

from users.domain.entities import UserEntity
from users.domain.exceptions import UserCreateFailed, UserNotFound
from users.domain.interfaces import IUserRepo
from users.models import Users


class DjangoOrmUserRepo(IUserRepo):
    def get(self, user_id: int) -> UserEntity:
        try:
            return Users.objects.get(id=user_id).to_entity()
        except Users.DoesNotExist:
            raise UserNotFound(detail="User not found")

    def create(self, entity: UserEntity):
        try:
            Users.from_entity(entity).save()
        except IntegrityError:
            raise UserCreateFailed(detail="User already exists")

    def get_by_email_and_password(self, email: str, password: str) -> UserEntity:
        try:
            return Users.objects.get(email=email, password=password).to_entity()
        except Users.DoesNotExist:
            raise UserNotFound(detail="Check email or password")
