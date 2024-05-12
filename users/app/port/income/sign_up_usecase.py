from typing import Protocol


class ISignUpUseCase(Protocol):
    def execute(self, email: str, password: str) -> None:
        ...
