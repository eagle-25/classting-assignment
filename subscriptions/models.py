from __future__ import annotations

from django.db import models

from subscriptions.domain.entities import SubscriptionEntity
from users.models import Users


class Subscriptions(models.Model):
    """
    구독 정보를 저장하는 테이블. publisher를 구독하는 사용자들을 저장한다.
    """

    id = models.SmallAutoField(primary_key=True)
    publisher = models.ForeignKey(Users, on_delete=models.DO_NOTHING, related_name="publisher")
    subscriber = models.ForeignKey(Users, on_delete=models.DO_NOTHING, related_name="subscriber")
    is_deleted = models.BooleanField(default=False)  # 구독 취소 여부
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)  # 구독 취소 시간

    class Meta:
        db_table = "subscriptions"
        constraints = [models.UniqueConstraint(fields=["publisher_id", "subscriber_id"], name="unique_user_publisher")]

    @classmethod
    def from_entity(cls, entity: SubscriptionEntity) -> Subscriptions:
        return cls(
            id=entity.id,
            publisher_id=entity.publisher_id,
            subscriber_id=entity.subscriber_id,
            is_deleted=entity.is_deleted,
        )

    def to_entity(self) -> SubscriptionEntity:
        return SubscriptionEntity(
            id=self.id,
            publisher_id=self.publisher.id,
            subscriber_id=self.subscriber.id,
            is_deleted=self.is_deleted,
            created_at=self.created_at,
            deleted_at=self.deleted_at,
        )
