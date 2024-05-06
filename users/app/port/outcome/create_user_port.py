from typing import Protocol


class ICreateUserPort(Protocol):
    def create_user(self, email: str, password: str) -> None:
        ...
