from dataclasses import dataclass, field
from datetime import datetime

from users.domain.values import UserType


@dataclass(kw_only=True)
class UserEntity:
    id: int | None = field(default=None)
    email: str
    password: str
    user_type: UserType
    created_at: datetime | None = field(default=None)
    updated_at: datetime | None = field(default=None)
