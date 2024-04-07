from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(kw_only=True, frozen=True)
class SchoolDTO:
    id: int
    name: str
    city: str
    owner_id: int
    owner_email: str
    created_at: datetime
