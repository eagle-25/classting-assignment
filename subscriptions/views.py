import jwt
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View

from common import settings
from common.exceptions import InvalidParameter, ValueNotFound
from subscriptions.adapters.repos.django_subscription_repo import (
    DjangoOrmSubscriptionRepo,
)
from subscriptions.usecases.subscription_usecaes import (
    create_subscription_usecase,
    delete_subscription_usecase,
    get_publisher_ids_usecase,
)
from users.domain.values import UserType


def _pare_user_id_and_type(jwt_token: str) -> tuple[int, str]:
    decoded_jwt = jwt.decode(jwt_token, key=settings.AES_KEY, algorithms=["HS256"])
    if (user_id := decoded_jwt.get("id")) is None:
        raise ValueNotFound(detail="user_id not found")
    if (user_type := decoded_jwt.get("type")) is None:
        raise ValueNotFound(detail="user_type not found")
    return user_id, user_type


class SubscriptionsView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        """
        구독 생성 API
        ---
        POST 요청으로 subscriber_id, publisher_id를 받아 구독을 생성한다.
        """
        # 유저 정보 파싱
        if (jwt_token := request.headers.get("Authorization")) is None:
            raise ValueNotFound(detail="Authorization header not found")
        user_id, user_type = _pare_user_id_and_type(jwt_token)
        if user_type != UserType.SUBSCRIBER.value:
            raise InvalidParameter(detail="User should be SUBSCRIBER")  # 기대한 유저 타입이 아닌 경우 에러 발생

        # publisher_id 파싱
        if (publisher_id := request.POST.get("publisher_id")) is None:
            raise ValueNotFound(detail="publisher_id not found")

        # 구독 생성
        create_subscription_usecase(
            subscription_repo=DjangoOrmSubscriptionRepo(),
            subscriber_id=user_id,
            publisher_id=int(publisher_id),
        )
        return HttpResponse(status=201)

    def get(self, request: HttpRequest) -> HttpResponse:
        if (jwt_token := request.headers.get("Authorization")) is None:
            raise ValueNotFound(detail="Authorization header not found")
        user_id, user_type = _pare_user_id_and_type(jwt_token)
        if user_type != UserType.SUBSCRIBER.value:
            raise InvalidParameter(detail="User should be SUBSCRIBER")  # 기대한 유저 타입이 아닌 경우 에러 발생

        publisher_ids = get_publisher_ids_usecase(subscription_repo=DjangoOrmSubscriptionRepo(), subscriber_id=user_id)
        return JsonResponse({"publisher_ids": publisher_ids}, status=200)

    def delete(self, request: HttpRequest, publisher_id: int) -> HttpResponse:
        if (jwt_token := request.headers.get("Authorization")) is None:
            raise ValueNotFound(detail="Authorization header not found")
        user_id, user_type = _pare_user_id_and_type(jwt_token)
        if user_type != UserType.SUBSCRIBER.value:
            raise InvalidParameter(detail="User should be SUBSCRIBER")  # 기대한 유저 타입이 아닌 경우 에러 발생

        delete_subscription_usecase(
            subscription_repo=DjangoOrmSubscriptionRepo(),
            subscriber_id=user_id,
            publisher_id=int(publisher_id),
        )
        return HttpResponse(status=204)
