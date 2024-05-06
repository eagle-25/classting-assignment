from typing import Protocol

from django.db import IntegrityError

from users.adapter.outcome.persistence.models import Users
from users.domain.exceptions import UserAlreadyExists, UserNotFound
from users.domain.user_entity import UserEntity


class IUserRepo(Protocol):
    def create(self, email: str, encrypted_password: str) -> None:
        ...

    def get(self, email: str, password: str) -> UserEntity:
        ...


class DjangoOrmUserRepo(IUserRepo):
    def create(self, email: str, encrypted_password: str) -> None:
        try:
            Users.objects.create(email=email, password=encrypted_password)
        except IntegrityError:
            raise UserAlreadyExists(detail="email income use")

    def get(self, email: str, password: str) -> UserEntity:
        try:
            return Users.objects.get(email=email, password=password).to_entity()
        except Users.DoesNotExist:
            raise UserNotFound(detail="Check email or password")
