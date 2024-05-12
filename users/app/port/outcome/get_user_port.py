from typing import Protocol

from users.domain.user_entity import UserEntity


class IGetUserPort(Protocol):
    def get_user(self, email: str, password: str) -> UserEntity:
        ...
