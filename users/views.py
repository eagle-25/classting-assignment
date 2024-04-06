from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View

from common.exceptions import ValueNotFound
from users.adapters.repos.django_user_repo import DjangoOrmUserRepo
from users.usecases.user_usecase import sign_in_usecase, sign_up_usecase


class UsersView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if (email := request.POST.get("email")) is None:
            raise ValueNotFound(detail="email")
        if (password := request.POST.get("password")) is None:
            raise ValueNotFound(detail="password")
        sign_up_usecase(
            user_repo=DjangoOrmUserRepo(),
            email=email,
            password=password,
        )
        return HttpResponse(status=200)

    def get(self, request: HttpRequest) -> HttpResponse:
        if (email := request.GET.get("email")) is None:
            raise ValueNotFound(detail="email")
        if (password := request.GET.get("password")) is None:
            raise ValueNotFound(detail="password")
        jwt_token = sign_in_usecase(user_repo=DjangoOrmUserRepo(), email=email, password=password)
        return JsonResponse({"jwt_token": jwt_token}, status=200)
