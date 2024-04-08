import logging

from django.http import HttpRequest, HttpResponse, JsonResponse

from common.exceptions import ClasstingException

logger = logging.getLogger(__name__)


class ExceptionMiddleware:
    def __init__(self, get_response) -> None:  # type: ignore[no-untyped-def]
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        return self.get_response(request)

    def process_exception(self, request: HttpRequest, exception: Exception) -> JsonResponse | None:
        if isinstance(exception, ClasstingException):
            logger.exception(exception.msg)
            return JsonResponse(
                {
                    "code": f"E-{exception.code}",
                    "msg": exception.msg,
                    "detail": exception.detail,
                },
                status=exception.status,
            )
        else:
            return None
