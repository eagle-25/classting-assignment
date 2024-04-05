from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class SubscriptionEntity:
    id: int | None = field(default=None)
    publisher_id: int
    subscriber_id: int
    is_deleted: bool
    created_at: datetime | None = field(default=None)
    deleted_at: datetime | None = field(default=None)
