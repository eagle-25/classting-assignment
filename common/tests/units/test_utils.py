from datetime import datetime, timedelta, timezone

import jwt
import pytest
from freezegun import freeze_time

from common import settings
from common.exceptions import InvalidParameter
from common.utils import (
    decode_jwt,
    decrypt_aes,
    encode_jwt,
    encrypt_aes,
    is_valid_email,
    parse_body,
)


def test_encrypt_aes():
    """
    AES 암호화가 정상적으로 동작하는지 테스트한다.
    """
    # given
    data = "hello"
    key = settings.AES_KEY
    iv = settings.AES_IV
    # when
    res = encrypt_aes(data, key, iv)
    # then
    assert res != data


def test_decrypt_aes():
    """
    AES 복호화가 정상적으로 동작하는지 테스트한다.
    """
    # given
    data = "hello"
    key = settings.AES_KEY
    iv = settings.AES_IV
    encrypted_data = encrypt_aes(data, key, iv)
    # when
    res = decrypt_aes(encrypted_data, key, iv)
    # then
    assert res == data


def test_encode_jwt():
    """
    JWT를 정상적으로 생성하는지 테스트한다.
    """
    # given
    payload = {"id": 1}

    # when
    res = encode_jwt(payload)

    # then
    expected_jwt = jwt.encode(payload=payload, key=settings.AES_KEY, algorithm="HS256")
    assert res == expected_jwt


def test_decode_jwt():
    """
    JWT를 정상적으로 디코딩하는지 테스트한다.
    """
    # given
    payload = {"id": 1}
    jwt_token = str(jwt.encode(payload=payload, key=settings.AES_KEY, algorithm="HS256"))

    # when
    res = decode_jwt(jwt_token)

    # then
    assert res == payload


def test_decode_jwt_expired():
    """
    만료된 JWT를 디코딩하면 InvalidParameter 예외가 발생하는지 테스트한다.
    """
    with freeze_time("2024-01-01 00:00:00") as frozen_time:
        # given
        payload = {"id": 1, "exp": datetime.now(tz=timezone.utc) - timedelta(minutes=1)}
        encoded_jwt = str(jwt.encode(payload=payload, key=settings.AES_KEY, algorithm="HS256"))

        # when
        frozen_time.tick(delta=timedelta(minutes=2))

        # then
        with pytest.raises(InvalidParameter) as e:
            _ = decode_jwt(encoded_jwt)
        assert e.value.detail == "Token expired"


def test_decode_jwt_invalid():
    """
    유효하지 않은 JWT를 디코딩하면 InvalidParameter 예외가 발생하는지 테스트한다.
    """
    # given
    encoded_jwt = "invalid_jwt"

    # then
    with pytest.raises(InvalidParameter) as e:
        _ = decode_jwt(encoded_jwt)
    assert e.value.detail == "Invalid token"


def test_parse_body():
    """
    request body를 정상적으로 파싱하는지 테스트한다.
    """

    # given
    class HttpRequest:
        body = b'{"id": 1}'

    # when
    res = parse_body(request=HttpRequest())

    # then
    assert res == {"id": 1}


def test_parse_body_raise_error():
    """
    request body가 json 형식이 아닐 때, InvalidParameter 예외가 발생하는지 테스트한다.
    """

    # given
    class HttpRequest:
        body = b"invalid_json"

    # then
    with pytest.raises(InvalidParameter) as e:
        parse_body(request=HttpRequest())
    assert e.value.detail == "Invalid body"


@pytest.mark.parametrize("email, expected_result", [("abc@example.com", True), ("abc", False)])
def test_is_valid_email(email, expected_result):
    # when
    res = is_valid_email(email)

    # then
    assert res == expected_result
