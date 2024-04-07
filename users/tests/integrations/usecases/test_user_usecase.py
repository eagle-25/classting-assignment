from datetime import datetime, timedelta, timezone

import pytest
from pytest_mock import MockerFixture

from common import settings
from common.utils import encode_jwt, encrypt_aes
from users.adapters.repos.django_user_repo import DjangoOrmUserRepo
from users.domain.entities import UserEntity
from users.tests.factories import UserFactory
from users.usecases.user_usecase import sign_in_usecase, sign_up_usecase


def test_sign_up_usecase(mocker: MockerFixture):
    """
    사용자 생성 로직을 기대한대로 호출하는지 테스트한다.
    """
    # given
    mocked_create = mocker.patch.object(DjangoOrmUserRepo, "create")
    email = "abc@example.com"
    password = "password"

    # when
    sign_up_usecase(
        user_repo=DjangoOrmUserRepo(),
        email=email,
        password=password,
    )

    # then
    encrypted_password = encrypt_aes(data=password, key=settings.AES_KEY, iv=settings.AES_IV)
    entity = UserEntity(email=email, password=encrypted_password)
    mocked_create.assert_called_once_with(entity=entity)


@pytest.mark.django_db
def test_sign_in_usecase():
    """
    email과 password로 에 해당하는 사용자가 있을 때, jwt를 기대한대로 반환하는지 테스트한다.
    """

    def _get_expected_jwt(user_id: int) -> str:
        session_expire_minutes = 60
        return encode_jwt(
            {
                "id": user_id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=session_expire_minutes),
            }
        )

    # given
    email = "abc@example.com"
    password = "password"
    encrypted_password = encrypt_aes(data=password, key=settings.AES_KEY, iv=settings.AES_IV)
    user = UserFactory(email=email, password=encrypted_password)

    # when
    res = sign_in_usecase(user_repo=DjangoOrmUserRepo(), email=email, password=password)

    # then
    assert res == _get_expected_jwt(user_id=user.id)
