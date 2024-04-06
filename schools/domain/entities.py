from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class SchoolEntity:
    id: int | None = field(default=None)  # DB auto filled
    owner_id: int
    name: str
    city: str
    created_at: datetime | None = field(default=None)  # DB auto filled
