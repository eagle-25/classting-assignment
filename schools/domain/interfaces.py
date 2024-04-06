from typing import Protocol

from schools.domain.entities import SchoolEntity


class ISchoolRepo(Protocol):
    def create(self, entity: SchoolEntity) -> None:
        ...

    def list(self, owner_id: int) -> list[SchoolEntity]:
        ...
