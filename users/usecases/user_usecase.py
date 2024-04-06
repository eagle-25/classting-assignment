from datetime import datetime, timedelta, timezone

import jwt

from common import settings
from common.utils import encrypt_aes
from users.domain.entities import UserEntity
from users.domain.interfaces import IUserRepo
from users.domain.values import UserType


def sign_up_usecase(user_repo: IUserRepo, *, email: str, password: str, user_type: UserType) -> None:
    """
    email과 password로 사용자를 생성한다. password는 AES로 암호화한다.
    """
    encrypted_password = encrypt_aes(data=password, key=settings.AES_KEY, iv=settings.AES_IV)
    entity = UserEntity(email=email, password=encrypted_password, user_type=user_type)
    user_repo.create(entity=entity)


def sign_in_usecase(user_repo: IUserRepo, *, email: str, password: str) -> str:
    """
    email과 password로 로그인을 시도한다. 로그인이 성공하면 jwt를 반환한다.
    """
    SESSION_EXPIRE_MINUTES = 60
    encrypted_password = encrypt_aes(data=password, key=settings.AES_KEY, iv=settings.AES_IV)
    user = user_repo.get(email=email, password=encrypted_password)
    return str(
        jwt.encode(
            {
                "id": user.id,
                "type": user.user_type.value,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=SESSION_EXPIRE_MINUTES),
            },
            settings.AES_KEY,
            algorithm="HS256",
        )
    )
