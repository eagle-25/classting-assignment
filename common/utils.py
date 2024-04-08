from typing import Any

import jwt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

from common import settings
from common.exceptions import InvalidParameter


def encrypt_aes(data: str, key: str, iv: str) -> str:
    data: bytes = data.encode("utf-8")
    key: bytes = key.encode("utf-8")
    iv: bytes = iv.encode("utf-8")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data, AES.block_size)
    return cipher.encrypt(padded_data).hex()


def decrypt_aes(data: str, key: str, iv: str) -> str:
    data: bytes = bytes.fromhex(data)
    key: bytes = key.encode("utf-8")
    iv: bytes = iv.encode("utf-8")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(data)
    return unpad(decrypted_data, AES.block_size).decode()


def encode_jwt(payload: dict[str, Any]) -> str:
    return str(jwt.encode(payload, key=settings.AES_KEY, algorithm="HS256"))


def decode_jwt(jwt_token: str) -> dict[str, Any]:
    try:
        return jwt.decode(jwt_token, key=settings.AES_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise InvalidParameter(detail="Token expired")
    except jwt.InvalidTokenError:
        raise InvalidParameter(detail="Invalid token")


def is_valid_email(email: str) -> bool:
    try:
        EmailValidator()(email)
        return True
    except ValidationError:
        return False
