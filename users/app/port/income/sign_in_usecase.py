from typing import Protocol


class ISignInUseCase(Protocol):
    def execute(self, email: str, password: str) -> str:
        ...
