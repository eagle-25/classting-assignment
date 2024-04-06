from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from django.http import HttpRequest

from common.exceptions import InvalidParameter, ValueNotFound
from common.utils import decode_jwt
from users.domain.values import UserType

T = TypeVar("T")


def jwt_login(expected_user_type: UserType) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def _wrapper(request: HttpRequest, *args: dict[Any, Any], **kwargs: dict[Any, Any]) -> T:
            # jwt token parsing
            if (jwt_token := request.headers.get("Authorization")) is None:
                raise ValueNotFound(detail="Authorization header not found")
            decoded_jwt = decode_jwt(jwt_token=jwt_token)
            # get user_id, user_type
            if (user_id := decoded_jwt.get("id")) is None:
                raise ValueNotFound(detail="user_id not found")
            if (user_type := decoded_jwt.get("type")) is None:
                raise ValueNotFound(detail="user_type not found")
            # check user_type
            if user_type != expected_user_type.value:
                raise InvalidParameter(detail=f"User should be {expected_user_type.value}")
            return func(request, user_id, *args, **kwargs)

        return _wrapper

    return decorator
