from collections.abc import Iterator
from datetime import datetime, timezone

from subscriptions.domain.exceptions import (
    SubscriptionCreateFailed,
    SubscriptionNotFound,
)
from subscriptions.domain.interfaces import ISubscriptionRepo
from subscriptions.models import Subscriptions


class DjangoOrmSubscriptionRepo(ISubscriptionRepo):
    def create(self, subscriber_id: int, publisher_id: int) -> None:
        """
        publisher 와 subscriber 간의 구독을 생성한다.
        """
        try:
            subscription = Subscriptions.objects.get(subscriber_id=subscriber_id, publisher=publisher_id)
            if subscription.is_deleted:
                subscription.is_deleted = False
                subscription.deleted_at = None
                subscription.save()
            else:
                raise SubscriptionCreateFailed(detail="Subscription already exists")
        except Subscriptions.DoesNotExist:
            Subscriptions.objects.create(subscriber_id=subscriber_id, publisher_id=publisher_id)

    def delete(self, subscriber_id: int, publisher_id: int) -> None:
        subscription = Subscriptions.objects.filter(
            subscriber_id=subscriber_id, publisher_id=publisher_id, is_deleted=False
        )
        if subscription.exists():
            subscription.update(is_deleted=True, deleted_at=datetime.now(tz=timezone.utc))
        else:
            raise SubscriptionNotFound(detail=f"subscriber_id: {subscriber_id}, publisher_id: {publisher_id}")

    def get_publisher_ids(self, subscriber_id: int) -> Iterator[int]:
        subscriptions = Subscriptions.objects.filter(subscriber_id=subscriber_id, is_deleted=False).order_by(
            "publisher_id"
        )
        yield from [subscription.publisher_id for subscription in subscriptions]
