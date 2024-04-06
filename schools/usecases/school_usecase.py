from schools.domain.entities import SchoolEntity
from schools.domain.interfaces import ISchoolRepo


def create_school_usecase(school_repo: ISchoolRepo, owner_id: int, name: str, city: str):
    school_repo.create(entity=SchoolEntity(owner_id=owner_id, name=name, city=city))


def list_schools_usecase(school_repo: ISchoolRepo, owner_id: int) -> list[SchoolEntity]:
    return list(school_repo.list(owner_id=owner_id))
