from django.db import IntegrityError

from users.domain.entities import UserEntity
from users.domain.exceptions import UserAlreadyExists, UserNotFound
from users.domain.interfaces import IUserRepo
from users.models import Users


class DjangoOrmUserRepo(IUserRepo):
    def get(self, user_id: int) -> UserEntity:
        try:
            return Users.objects.get(id=user_id).to_entity()
        except Users.DoesNotExist:
            raise UserNotFound(detail="User not found")

    def create(self, email: str, encrypted_password: str) -> None:
        try:
            Users.objects.create(email=email, password=encrypted_password)
        except IntegrityError:
            raise UserAlreadyExists(detail="email in use")

    def get_by_email_and_password(self, email: str, password: str) -> UserEntity:
        try:
            return Users.objects.get(email=email, password=password).to_entity()
        except Users.DoesNotExist:
            raise UserNotFound(detail="Check email or password")
