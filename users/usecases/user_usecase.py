from datetime import datetime, timedelta, timezone

from common import settings
from common.exceptions import InvalidParameter
from common.utils import encode_jwt, encrypt_aes, is_valid_email
from users.domain.interfaces import IUserRepo


def sign_up_usecase(user_repo: IUserRepo, *, email: str, password: str) -> None:
    """
    email과 password로 사용자를 생성한다. password는 AES로 암호화한다.
    """
    if not is_valid_email(email):
        raise InvalidParameter(detail="Invalid email")
    else:
        encrypted_password = encrypt_aes(data=password, key=settings.AES_KEY, iv=settings.AES_IV)
        user_repo.create(email=email, encrypted_password=encrypted_password)


def sign_in_usecase(user_repo: IUserRepo, *, email: str, password: str) -> str:
    """
    email과 password로 로그인을 시도한다. 로그인이 성공하면 jwt를 반환한다.
    """
    if not is_valid_email(email):
        raise InvalidParameter(detail="Invalid email")
    else:
        SESSION_EXPIRE_MINUTES = 60
        encrypted_password = encrypt_aes(data=password, key=settings.AES_KEY, iv=settings.AES_IV)
        user = user_repo.get_by_email_and_password(email=email, password=encrypted_password)
        return encode_jwt(
            payload={
                "id": user.id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=SESSION_EXPIRE_MINUTES),
            }
        )
