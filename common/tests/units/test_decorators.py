from datetime import datetime, timedelta
from typing import Any

import pytest
from django.http import HttpRequest, HttpResponse
from django.test import RequestFactory
from freezegun import freeze_time

from common.decorators import jwt_login
from common.exceptions import Unauthorized
from common.utils import encode_jwt


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
        jwt = encode_jwt({"id": 1, "exp": datetime.now() + timedelta(minutes=1)})
        request = RequestFactory()
        request.COOKIES = {"jwt": jwt}

        # when
        res = jwt_login(mocked_http_view)(request)

        # then
        assert res.status_code == 200


def test_jwt_login_error_no_authorization_header():
    """
    쿠키에 jwt가 없을 때, Unauthorized 예외가 발생하는지 테스트한다.
    """
    # given
    request = RequestFactory()
    request.COOKIES = {}

    # when, then
    with pytest.raises(Unauthorized):
        jwt_login(mocked_http_view)(request)


def test_jwt_login_error_no_user_id():
    """
    user_id가 없을 때, Unauthorized 예외가 발생하는지 테스트한다.
    """
    # given
    jwt = encode_jwt({})
    request = RequestFactory()
    request.COOKIES = {"jwt": jwt}

    # when, then
    with pytest.raises(Unauthorized):
        jwt_login(mocked_http_view)(request)


def test_jwt_login_error_jwt_expired():
    """
    jwt가 만료되었을 때, Unauthorized 예외가 발생하는지 테스트한다.
    """
    with freeze_time("2024-01-01 00:00:00"):
        # given
        jwt = encode_jwt({"id": 1, "exp": datetime.now() - timedelta(minutes=1)})
        request = RequestFactory()
        request.COOKIES = {"jwt": jwt}

        # when, then
        with pytest.raises(Unauthorized):
            jwt_login(mocked_http_view)(request)


def test_jwt_login_error_invalid_jwt():
    """
    jwt가 유효하지 않을 때, Unauthorized 예외가 발생하는지 테스트한다.
    """
    # given
    jwt = "invalid_jwt"
    request = RequestFactory()
    request.COOKIES = {"jwt": jwt}

    # when, then
    with pytest.raises(Unauthorized):
        jwt_login(mocked_http_view)(request)
