from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from common.decorators import jwt_login
from common.exceptions import ValueNotFound
from subscriptions.adapters.repos.django_subscription_repo import (
    DjangoOrmSubscriptionRepo,
)
from subscriptions.usecases.subscription_usecaes import (
    CreateSubscriptionUsecase,
    DeleteSubscriptionUsecase,
    GetPublisherIdsUsecase,
)
from users.adapters.repos.django_user_repo import DjangoOrmUserRepo
from users.domain.values import UserType


class SubscriptionsView(View):
    @method_decorator(jwt_login(expected_user_type=UserType.SUBSCRIBER))
    def post(self, request: HttpRequest, user_id: int) -> HttpResponse:
        """
        구독 생성 API
        """
        if (publisher_id := request.POST.get("publisher_id")) is None:
            raise ValueNotFound(detail="publisher_id not found")
        usecase = CreateSubscriptionUsecase(
            subscription_repo=DjangoOrmSubscriptionRepo(),
            user_repo=DjangoOrmUserRepo(),
        )
        usecase.execute(subscriber_id=user_id, publisher_id=int(publisher_id))
        return HttpResponse(status=201)

    @method_decorator(jwt_login(expected_user_type=UserType.SUBSCRIBER))
    def get(self, request: HttpRequest, user_id: int) -> HttpResponse:
        """
        구독 조회 API
        """
        usecase = GetPublisherIdsUsecase(
            subscription_repo=DjangoOrmSubscriptionRepo(),
            user_repo=DjangoOrmUserRepo(),
        )
        publisher_ids = usecase.execute(subscriber_id=user_id)
        return JsonResponse({"publisher_ids": publisher_ids}, status=200)

    @method_decorator(jwt_login(expected_user_type=UserType.SUBSCRIBER))
    def delete(self, request: HttpRequest, user_id: int, publisher_id: int) -> HttpResponse:
        """
        구독 삭제 API
        """
        usecase = DeleteSubscriptionUsecase(
            subscription_repo=DjangoOrmSubscriptionRepo(),
            user_repo=DjangoOrmUserRepo(),
        )
        usecase.execute(subscriber_id=user_id, publisher_id=publisher_id)
        return HttpResponse(status=204)
