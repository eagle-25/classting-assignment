import logging
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse

from common.exceptions import ArgumentMissingException

logger = logging.getLogger(__name__)


class ArgumentMissingMiddleware:
    def __init__(self, get_response: Any) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception) -> HttpResponse | None:
        if isinstance(exception, TypeError) and 'missing 1 required positional argument' in str(exception):
            logger.exception(str(exception))
            keyword = str(exception).split(":")[1].strip()
            e = ArgumentMissingException(detail=keyword)
            return JsonResponse(
                {
                    "code": f"E-{e.code}",
                    "msg": e.msg,
                    "detail": e.detail,
                }
            )
        else:
            return None
