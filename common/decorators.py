from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from django.http import HttpRequest

from common.exceptions import ValueNotFound
from common.utils import decode_jwt

T = TypeVar("T")


def jwt_login() -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def _wrapper(request: HttpRequest, *args: dict[Any, Any], **kwargs: dict[Any, Any]) -> T:
            # jwt token parsing
            if (jwt_token := request.headers.get("Authorization")) is None:
                raise ValueNotFound(detail="Authorization header not found")
            decoded_jwt = decode_jwt(jwt_token=jwt_token)
            # get user_id
            if (user_id := decoded_jwt.get("id")) is None:
                raise ValueNotFound(detail="user_id not found")
            return func(request, user_id, *args, **kwargs)

        return _wrapper

    return decorator
