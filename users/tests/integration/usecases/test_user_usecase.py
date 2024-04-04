from datetime import datetime, timedelta, timezone

import jwt
import pytest

from common import settings
from users.adapters.repos.django_user_repo import DjangoOrmUserRepo
from users.domain.values import UserType
from users.models import Users
from users.tests.factories import UsersFactory
from users.usecases.user_usecase import sign_in_usecase, sign_up_usecase
from users.utils import encrypt_aes


@pytest.mark.django_db
def test_sign_up_usecase():
    """
    email과 password로 사용자를 생성하는지 테스트한다. 암호는 암호화 되어 저장되었는지 테스트한다.
    """
    # given
    email = "abc@example.com"
    password = "password"

    # when
    sign_up_usecase(
        user_repo=DjangoOrmUserRepo(),
        email=email,
        password=password,
        user_type=UserType.PUBLISHER,
    )

    # then
    encrypted_password = encrypt_aes(
        data=password, key=settings.AES_KEY, iv=settings.AES_IV
    )
    assert Users.objects.filter(email=email, password=encrypted_password).exists()


@pytest.mark.django_db
def test_sign_in_usecase():
    """
    email과 password로 에 해당하는 사용자가 있을 때, jwt를 기대한대로 반환하는지 테스트한다.
    """

    def _get_expected_jwt(user_id: int) -> str:
        session_expire_minutes = 60
        return jwt.encode(
            {
                "id": user_id,
                "exp": datetime.now(tz=timezone.utc)
                + timedelta(minutes=session_expire_minutes),
            },
            settings.AES_KEY,
            algorithm="HS256",
        )

    # given
    email = "abc@example.com"
    password = "password"
    encrypted_password = encrypt_aes(
        data=password, key=settings.AES_KEY, iv=settings.AES_IV
    )
    user = UsersFactory(
        email=email, password=encrypted_password, user_type=UserType.PUBLISHER
    )

    # when
    res = sign_in_usecase(user_repo=DjangoOrmUserRepo(), email=email, password=password)

    # then
    assert res == _get_expected_jwt(user_id=user.id)
