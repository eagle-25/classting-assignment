from __future__ import annotations

from django.db import models

from subscriptions.domain.entities import SubscriptionEntity


class Subscriptions(models.Model):
    """
    구독 관계를 저장하는 테이블. school을 구독하는 user 정보를 저장한다.
    """

    id = models.SmallAutoField(primary_key=True)
    user = models.ForeignKey("users.Users", on_delete=models.DO_NOTHING, null=False)
    school = models.ForeignKey("schools.Schools", on_delete=models.DO_NOTHING, null=False)
    subscribed_at = models.DateTimeField(null=False)  # 구독 시작 시간
    canceled_at = models.DateTimeField(null=True)  # 구독 취소 시간, 구독 중이면 None

    class Meta:
        db_table = "subscriptions"
        unique_together = [["user_id", "school_id"]]

    @classmethod
    def from_entity(cls, entity: SubscriptionEntity) -> Subscriptions:
        return cls(
            user_id=entity.user_id,
            school_id=entity.school_id,
            subscribed_at=entity.subscribed_at,
            canceled_at=entity.canceled_at,
        )

    def to_entity(self) -> SubscriptionEntity:
        return SubscriptionEntity(
            id=self.id,
            user_id=self.user.id,
            school_id=self.school.id,
            subscribed_at=self.subscribed_at,
            canceled_at=self.canceled_at,
        )
