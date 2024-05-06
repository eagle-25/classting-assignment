from datetime import datetime, timedelta, timezone

from common import settings
from common.utils import encode_jwt, encrypt_aes
from users.app.port.income.sign_in_usecase import ISignInUseCase
from users.app.port.outcome.get_user_port import IGetUserPort


class SignInUseCase(ISignInUseCase):
    def __init__(self, get_user_port: IGetUserPort):
        self._get_user_port = get_user_port

    def execute(self, email: str, password: str) -> str:
        """
        email과 password로 로그인을 시도한다. 로그인이 성공하면 jwt를 반환한다.
        """
        SESSION_EXPIRE_MINUTES = 60
        encrypted_password = encrypt_aes(data=password, key=settings.AES_KEY, iv=settings.AES_IV)
        user = self._get_user_port.get_user(email=email, password=encrypted_password)
        return encode_jwt(
            payload={
                "id": user.id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=SESSION_EXPIRE_MINUTES),
            }
        )
