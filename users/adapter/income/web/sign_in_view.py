from django.http import HttpRequest, HttpResponse
from django.views import View

from common.exceptions import ValueNotFound
from users.app.port.income.sign_in_usecase import ISignInUseCase


class SignInView(View):
    def __init__(self, usecase: ISignInUseCase):
        self._usecase = usecase

    def handle(self, request: HttpRequest) -> HttpResponse:
        if (email := request.POST.get('email')) is None:
            raise ValueNotFound('email is required')
        if (password := request.POST.get('password')) is None:
            raise ValueNotFound('password is required')
        jwt = self._usecase.execute(email, password)

        response = HttpResponse()
        response.set_cookie('jwt', jwt)
        return response
