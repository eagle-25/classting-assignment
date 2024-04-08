from dataclasses import dataclass


@dataclass(kw_only=True)
class SearchSchoolsCmd:
    owner_id: int | None = None
    school_name: str | None = None
    city: str | None = None
