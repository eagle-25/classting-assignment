from django.http import HttpRequest, JsonResponse

from common.exceptions import ClasstingException


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(
        self, request: HttpRequest, exception: Exception
    ) -> JsonResponse | None:
        if isinstance(exception, ClasstingException):
            return JsonResponse(
                {
                    "code": exception.code,
                    "msg": exception.msg,
                    "detail": exception.detail,
                },
                status=exception.status,
            )
        else:
            return None
