from django.http import HttpRequest, HttpResponse

from common.exceptions import ValueNotFound
from users.adapters.repos.django_user_repo import DjangoOrmUserRepo
from users.usecases.user_usecase import sign_in_usecase, sign_up_usecase


def sign_in_view(request: HttpRequest) -> HttpResponse:
    if (email := request.POST.get("email")) is None:
        raise ValueNotFound(detail="email")
    if (password := request.POST.get("password")) is None:
        raise ValueNotFound(detail="password")
    jwt_token = sign_in_usecase(user_repo=DjangoOrmUserRepo(), email=email, password=password)
    resp = HttpResponse(status=200)
    resp.set_cookie("jwt", jwt_token, httponly=True)
    return resp


def sign_up_view(request: HttpRequest) -> HttpResponse:
    if (email := request.POST.get("email")) is None:
        raise ValueNotFound(detail="email")
    if (password := request.POST.get("password")) is None:
        raise ValueNotFound(detail="password")
    sign_up_usecase(user_repo=DjangoOrmUserRepo(), email=email, password=password)
    return HttpResponse(status=201)
