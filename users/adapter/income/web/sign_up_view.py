from django.http import HttpRequest, HttpResponse

from common.exceptions import ValueNotFound
from users.app.port.income.sign_up_usecase import ISignUpUseCase


class SignUpView:
    def __init__(self, usecase: ISignUpUseCase):
        self._usecase = usecase

    def handle(self, request: HttpRequest) -> HttpResponse:
        if (email := request.POST.get('email')) is None:
            raise ValueNotFound('email is required')
        if (password := request.POST.get('password')) is None:
            raise ValueNotFound('password is required')
        self._usecase.execute(email, password)
        return HttpResponse(status=201)
