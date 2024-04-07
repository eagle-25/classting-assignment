from collections.abc import Iterable
from datetime import datetime, timezone

from django.core.paginator import Paginator
from django.db import IntegrityError

from schools.domain.entities import SchoolNewsEntity
from schools.models import SchoolNews
from subscriptions.domain.entities import SubscriptionEntity
from subscriptions.domain.exceptions import (
    SubscriptionCancelFailed,
    SubscriptionCreateFailed,
)
from subscriptions.domain.interfaces import ISubscriptionsRepo
from subscriptions.models import Subscriptions
from users.domain.exceptions import UserNotFound
from users.models import Users


class DjangoOrmSubscriptionsRepo(ISubscriptionsRepo):
    def create_subscription(self, user_id: int, school_id: int) -> None:
        """
        구독을 생성한다.
        """

        def _create_subscription(user_id_: int, school_id_: int) -> None:
            """
            최초 구독시 사용
            """
            entity = SubscriptionEntity(
                user_id=user_id_,
                school_id=school_id_,
                subscribed_at=datetime.now(tz=timezone.utc),
                canceled_at=None,
            )
            try:
                Subscriptions.from_entity(entity=entity).save()
            except IntegrityError:
                raise SubscriptionCreateFailed(detail="Already subscribed")

        def _reactivate_subscription(subscription_: Subscriptions) -> None:
            """
            재구독시 사용
            """
            subscription_.subscribed_at = datetime.now(tz=timezone.utc)
            subscription_.canceled_at = None
            subscription_.save()

        # 기 구독 여부 조회
        subscription = Subscriptions.objects.filter(user_id=user_id, school_id=school_id).first()
        # 최초 구독 --> 새로 생성
        if subscription is None:
            _create_subscription(user_id, school_id)
        # 재구독 --> 구독 취소 시간 초기화
        elif subscription.canceled_at is not None:
            _reactivate_subscription(subscription)
        # 이미 구독한 경우 --> 에러 발생
        else:
            raise SubscriptionCreateFailed(detail="Already subscribed")

    def list_subscriptions(self, user_id: int) -> list[SubscriptionEntity]:
        """
        구독증인 학교 목록을 조회한다.
        """
        return [x.to_entity() for x in Subscriptions.objects.filter(user_id=user_id, canceled_at__isnull=True)]

    def cancel_subscription(self, user_id: int, school_id: int) -> None:
        """
        학교 구독을 취소한다.
        """
        subscription = Subscriptions.objects.filter(user_id=user_id, school_id=school_id).first()
        # 구독 없는 경우
        if subscription is None:
            raise SubscriptionCancelFailed(detail="Subscription not found")
        # 이미 취소한 경우
        elif subscription.canceled_at is not None:
            raise SubscriptionCancelFailed(detail="Already canceled")
        # 구독 취소
        else:
            subscription.canceled_at = datetime.now(tz=timezone.utc)
            subscription.save()

    def iter_subscribed_schools_news(
        self, user_id: int, page_index: int = 1, page_size: int = 10
    ) -> tuple[int, Iterable[SchoolNewsEntity]]:  # page_cnt, news
        """
        구독한 학교들의 소식을 최신순으로 가져온다. 소식은 구독을 시작한 시점 ~ 취소한 시점까지만 가져와야 한다.
        """
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            raise UserNotFound

        subscriptions = Subscriptions.objects.filter(user=user)
        news = SchoolNews.objects.none()
        for subscription in subscriptions:

            news |= SchoolNews.objects.filter(
                school=subscription.school,
                created_at__gte=subscription.subscribed_at,
                created_at__lte=subscription.canceled_at or datetime.now(tz=timezone.utc),
            )
        news = news.order_by('-created_at')
        paginator = Paginator(news, page_size)
        return paginator.num_pages, [x.to_entity() for x in paginator.page(page_index).object_list]
