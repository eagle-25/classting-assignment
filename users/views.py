from django.http import HttpRequest, HttpResponse, JsonResponse

from common.exceptions import ValueNotFound
from users.adapters.repos.django_user_repo import DjangoOrmUserRepo
from users.domain.values import UserType
from users.usecases.user_usecase import sign_in_usecase, sign_up_usecase


def sign_up_view(request: HttpRequest) -> HttpResponse:
    if (email := request.POST.get("email")) is None:
        raise ValueNotFound(detail="email")
    if (password := request.POST.get("password")) is None:
        raise ValueNotFound(detail="password")
    sign_up_usecase(
        user_repo=DjangoOrmUserRepo(),
        email=email,
        password=password,
        user_type=UserType.PUBLISHER,
    )
    return HttpResponse(status=200)


def sign_in_view(request: HttpRequest) -> HttpResponse:
    if (email := request.POST.get("email")) is None:
        raise ValueNotFound(detail="email")
    if (password := request.POST.get("password")) is None:
        raise ValueNotFound(detail="password")
    jwt = sign_in_usecase(user_repo=DjangoOrmUserRepo(), email=email, password=password)
    return JsonResponse({"jwt_token": jwt}, status=200)
