from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class UserEntity:
    id: int | None = field(default=None)
    email: str
    password: str
    created_at: datetime | None = field(default=None)
    updated_at: datetime | None = field(default=None)
