import dataclasses

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from common.decorators import jwt_login
from common.exceptions import ValueNotFound
from subscriptions.adapters.repos.subscriptions_repo import DjangoOrmSubscriptionsRepo
from subscriptions.usecases.subscription_usecases import create_subscription_usecase


class SubscriptionsView(View):
    @method_decorator(jwt_login)
    def post(self, request: HttpRequest, user_id: int) -> HttpResponse:
        """
        구독 생성 API
        """
        if (school_id := request.POST.get('school_id')) is None:
            raise ValueNotFound(detail="school_id")
        repo = DjangoOrmSubscriptionsRepo()
        create_subscription_usecase(subscription_repo=repo, user_id=user_id, school_id=int(school_id))
        return HttpResponse(status=201)

    @method_decorator(jwt_login)
    def get(self, request: HttpRequest, user_id: int) -> HttpResponse:
        """
        구독 목록 조회 API
        """
        repo = DjangoOrmSubscriptionsRepo()
        subscriptions = repo.list_subscriptions(user_id=user_id)
        subscriptions = [
            {"school_id": subscription.school_id, "subscribed_at": subscription.subscribed_at}
            for subscription in subscriptions
        ]
        return JsonResponse({"subscriptions": subscriptions})

    @method_decorator(jwt_login)
    def delete(self, request: HttpRequest, user_id: int, school_id: int) -> HttpResponse:
        """
        구독 삭제 API
        """
        repo = DjangoOrmSubscriptionsRepo()
        repo.cancel_subscription(user_id=user_id, school_id=school_id)
        return HttpResponse(status=204)


@jwt_login
def list_school_news(request: HttpRequest, user_id: int) -> HttpResponse:
    """
    학교 소식 목록 조회 API
    """
    NEWS_PAGE_SIZE = 10
    page = int(request.GET.get('page_index', 1))
    page_cnt, news = DjangoOrmSubscriptionsRepo().iter_subscribed_schools_news(
        user_id=user_id, page_index=page, page_size=NEWS_PAGE_SIZE
    )
    news = [dataclasses.asdict(news) for news in news]
    return JsonResponse({"page_size": NEWS_PAGE_SIZE, "total_page_cnt": page_cnt, "cur_page_index": page, "news": news})
