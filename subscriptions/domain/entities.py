from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class SubscriptionEntity:
    id: int
    user_id: int
    school_id: int
    subscribed_at: datetime
    canceled_at: datetime | None = field(default=None)
