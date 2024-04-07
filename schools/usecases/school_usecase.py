from common.exceptions import Unauthorized
from schools.domain.commands import ListSchoolsCmd
from schools.domain.entities import SchoolEntity, SchoolNewsEntity
from schools.domain.interfaces import ISchoolRepo
from schools.values import SchoolDTO


def create_school_usecase(school_repo: ISchoolRepo, owner_id: int, name: str, city: str) -> None:
    """
    학교를 생성하는 유스케이스
    """
    school_repo.create_school(entity=SchoolEntity(owner_id=owner_id, name=name, city=city))


def list_schools_usecase(school_repo: ISchoolRepo, cmd: ListSchoolsCmd) -> list[SchoolDTO]:
    """
    해당하는 학교들을 조회하는 유스케이스
    """
    return school_repo.list_schools(cmd)


def create_school_news_usecase(school_repo: ISchoolRepo, owner_id: int, school_id: int, content: str) -> None:
    """
    학교 소식을 생성하는 유스케이스
    """
    if school_repo.is_owned_school(owner_id=owner_id, school_id=school_id):
        entity = SchoolNewsEntity(school_id=school_id, content=content)
        school_repo.create_school_news(entity=entity)
    else:
        raise Unauthorized


def list_school_news_usecase(school_repo: ISchoolRepo, school_id: int) -> list[SchoolNewsEntity]:
    """
    학교 소식들을 조회해 최신순으로 반환하는 유스케이스
    """
    return school_repo.list_school_news(school_id=school_id)


def update_school_news_usecase(school_repo: ISchoolRepo, owner_id: int, news_id: int, content: str) -> SchoolNewsEntity:
    """
    학교 소식을 수정하는 유스케이스
    """
    if not school_repo.is_owned_news(owner_id=owner_id, news_id=news_id):
        raise Unauthorized
    else:
        return school_repo.update_school_news(news_id=news_id, content=content)


def delete_school_news_usecase(school_repo: ISchoolRepo, owner_id: int, news_id: int) -> None:
    """
    학교 소식을 삭제하는 유스케이스
    """
    if not school_repo.is_owned_news(owner_id=owner_id, news_id=news_id):
        raise Unauthorized
    else:
        school_repo.delete_school_news(news_id=news_id)
