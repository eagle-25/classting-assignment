from common.exceptions import Unauthorized
from schools.domain.entities import SchoolNewsEntity
from schools.domain.interfaces import ISchoolRepo


def create_school_news_usecase(school_repo: ISchoolRepo, owner_id: int, school_id: int, content: str) -> None:
    """
    학교 소식을 생성하는 유스케이스
    """
    if not school_repo.is_owned_school(owner_id=owner_id, school_id=school_id):
        raise Unauthorized
    else:
        entity = SchoolNewsEntity(school_id=school_id, content=content)
        school_repo.create_school_news(entity=entity)


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
