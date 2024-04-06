from datetime import datetime, timedelta
from typing import Any

import pytest
from django.http import HttpRequest, HttpResponse
from django.test import RequestFactory
from freezegun import freeze_time

from common.decorators import jwt_login
from common.exceptions import InvalidParameter, ValueNotFound
from common.utils import encode_jwt
from users.domain.values import UserType


def mocked_http_view(
    request: HttpRequest, user_id: int, *args: dict[Any, Any], **kwargs: dict[Any, Any]
) -> HttpResponse:
    return HttpResponse(status=200)


def test_jwt_login():
    """
    jwt_login이 정상 작동하는지 테스트한다.
    """
    with freeze_time("2024-01-01 00:00:00"):
        # given
        jwt = encode_jwt({"id": 1, "type": UserType.PUBLISHER.value, "exp": datetime.now() + timedelta(minutes=1)})
        request = RequestFactory().get("/", headers={"Authorization": jwt})

        # when
        res = jwt_login(expected_user_type=UserType.PUBLISHER)(mocked_http_view)(request)

        # then
        assert res.status_code == 200


def test_jwt_login_error_no_authorization_header():
    """
    Authorization 헤더가 없을 때, ValueNotFound 예외가 발생하는지 테스트한다.
    """
    # given
    request = RequestFactory().get("/")

    # when, then
    with pytest.raises(ValueNotFound) as e:
        jwt_login(expected_user_type=UserType.PUBLISHER)(mocked_http_view)(request)
    assert e.value.detail == "Authorization header not found"


def test_jwt_login_error_no_user_id():
    """
    user_id가 없을 때, ValueNotFound 예외가 발생하는지 테스트한다.
    """
    # given
    jwt = encode_jwt({"type": UserType.PUBLISHER.value})
    request = RequestFactory().get("/", headers={"Authorization": jwt})

    # when, then
    with pytest.raises(ValueNotFound) as e:
        jwt_login(expected_user_type=UserType.PUBLISHER)(mocked_http_view)(request)
    assert e.value.detail == "user_id not found"


def test_jwt_login_error_no_user_type():
    """
    user_type이 없을 때, ValueNotFound 예외가 발생하는지 테스트한다.
    """
    # given
    jwt = encode_jwt({"id": 1})
    request = RequestFactory().get("/", headers={"Authorization": jwt})

    # when, then
    with pytest.raises(ValueNotFound) as e:
        jwt_login(expected_user_type=UserType.PUBLISHER)(mocked_http_view)(request)
    assert e.value.detail == "user_type not found"


def test_jwt_login_error_invalid_user_type():
    """
    user_type이 다를 때, InvalidParameter 예외가 발생하는지 테스트한다.
    """
    # given
    jwt = encode_jwt({"id": 1, "type": UserType.SUBSCRIBER.value})
    request = RequestFactory().get("/", headers={"Authorization": jwt})

    # when, then
    with pytest.raises(InvalidParameter) as e:
        jwt_login(expected_user_type=UserType.PUBLISHER)(mocked_http_view)(request)
    assert e.value.detail == "User should be publisher"
