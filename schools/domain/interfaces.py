from collections.abc import Iterable
from typing import Protocol

from schools.domain.entities import SchoolEntity, SchoolNewsEntity


class ISchoolRepo(Protocol):
    def create_school(self, entity: SchoolEntity) -> None:
        ...

    def list_school(self, owner_id: int) -> Iterable[SchoolEntity]:
        ...

    def create_school_news(self, entity: SchoolNewsEntity) -> None:
        ...

    def list_school_news(self, school_id: int) -> Iterable[SchoolNewsEntity]:
        ...

    def update_school_news(self, news_id: int, content: str) -> SchoolNewsEntity:
        ...

    def delete_school_news(self, news_id: int) -> None:
        ...

    def is_owned_news(self, owner_id: int, news_id: int) -> bool:
        ...

    def is_owned_school(self, owner_id: int, school_id: int) -> bool:
        ...
