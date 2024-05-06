from datetime import datetime, timedelta, timezone

from common.utils import encode_jwt
from users.app.port.outcome.get_user_port import IGetUserPort
from users.app.usecase.sign_in_usecase import SignInUseCase


def test_sgin_in_usecase_call_get_user(mocker, user):
    """
    IGetUserPort.get_user()를 기대한대로 호출하는지 테스트한다.
    """
    # arrange
    mocker.patch("users.app.usecase.sign_in_usecase.encrypt_aes", return_value=user.password)

    get_user_adapter = mocker.Mock(spec=IGetUserPort)
    get_user_adapter.get_user.return_value = user

    usecase = SignInUseCase(get_user_port=get_user_adapter)

    # act
    _ = usecase.execute(email=user.email, password=user.password)

    # assert
    get_user_adapter.get_user.assert_called_once_with(email=user.email, password=user.password)


def test_sign_in_usecase_return_jwt(mocker, user):
    """
    jwt를 반환하는지 테스트한다.
    """

    def _get_expected_jwt(user_id: int) -> str:
        SESSION_EXPIRE_MINUTES = 60
        return encode_jwt(
            payload={
                "id": user_id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=SESSION_EXPIRE_MINUTES),
            }
        )

    # arrange
    get_user_adapter = mocker.Mock(spec=IGetUserPort)
    get_user_adapter.get_user.return_value = user

    usecase = SignInUseCase(get_user_port=get_user_adapter)

    # act
    res = usecase.execute(email=user.email, password=user.password)

    # assert
    assert res == _get_expected_jwt(user.id)
