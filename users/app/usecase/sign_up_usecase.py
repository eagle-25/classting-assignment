from common import settings
from common.utils import encrypt_aes
from users.app.port.income.sign_up_usecase import ISignUpUseCase
from users.app.port.outcome.create_user_port import ICreateUserPort


class SignUpUsecase(ISignUpUseCase):
    def __init__(self, create_user_port: ICreateUserPort):
        self._create_user_port = create_user_port

    def execute(self, email: str, password: str) -> None:
        """
        email과 password로 사용자를 생성한다. password는 AES로 암호화한다.
        """
        encrypted_password = encrypt_aes(data=password, key=settings.AES_KEY, iv=settings.AES_IV)
        self._create_user_port.create_user(email=email, password=encrypted_password)
