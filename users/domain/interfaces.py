from typing import Protocol

from users.domain.entities import UserEntity


class IUserRepo(Protocol):
    def get(self, email: str, password: str) -> UserEntity: ...

    def create(self, entity: UserEntity) -> None: ...
