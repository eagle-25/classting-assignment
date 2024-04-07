from dataclasses import dataclass


@dataclass(kw_only=True)
class ListSchoolsCmd:
    owner_id: int | None = None
    school_name: str | None = None
    city: str | None = None
