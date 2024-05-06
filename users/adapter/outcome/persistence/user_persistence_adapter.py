from users.adapter.outcome.persistence.user_repo import IUserRepo
from users.app.port.outcome.create_user_port import ICreateUserPort
from users.app.port.outcome.get_user_port import IGetUserPort
from users.domain.user_entity import UserEntity


class UserPersistenceAdapter(ICreateUserPort, IGetUserPort):
    def __init__(self, user_repo: IUserRepo):
        self._user_repo = user_repo

    def create_user(self, email: str, password: str) -> None:
        self._user_repo.create(email, password)

    def get_user(self, email: str, password: str) -> UserEntity:
        return self._user_repo.get(email, password)
