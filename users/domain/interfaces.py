from typing import Protocol

from users.domain.entities import UserEntity


class IUserRepo(Protocol):
    def get(self, user_id: int) -> UserEntity:
        ...

    def create(self, entity: UserEntity) -> None:
        ...

    def get_by_email_and_password(self, email: str, password: str) -> UserEntity:
        ...
