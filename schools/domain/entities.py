from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class SchoolEntity:
    id: int | None = field(default=None)  # DB auto filled
    owner_id: int
    name: str
    city: str
    created_at: datetime | None = field(default=None)  # DB auto filled


@dataclass(kw_only=True)
class SchoolNewsEntity:
    id: int | None = field(default=None)
    school_id: int
    content: str
    created_at: datetime | None = field(default=None)
    updated_at: datetime | None = field(default=None)
