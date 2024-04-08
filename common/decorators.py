from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from django.http import HttpRequest

from common.exceptions import InvalidParameter, Unauthorized
from common.utils import decode_jwt

T = TypeVar("T")


def jwt_login(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def _wrapper(request: HttpRequest, *args: dict[Any, Any], **kwargs: dict[Any, Any]) -> T:
        # jwt token parsing
        if (jwt_token := request.COOKIES.get("jwt")) is None:
            raise Unauthorized
        # jwt decoding
        try:
            decoded_jwt = decode_jwt(jwt_token=jwt_token)
        except InvalidParameter:
            raise Unauthorized
        # get user_id
        if (user_id := decoded_jwt.get("id")) is None:
            raise Unauthorized(detail="user_id not found")
        return func(request, user_id, *args, **kwargs)

    return _wrapper
