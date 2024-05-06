from dataclasses import dataclass
from datetime import datetime


@dataclass(kw_only=True)
class UserEntity:
    id: int
    email: str
    password: str
    created_at: datetime
    updated_at: datetime
