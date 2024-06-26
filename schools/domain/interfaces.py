from typing import Protocol

from schools.domain.commands import SearchSchoolsCmd
from schools.domain.entities import SchoolNewsEntity
from schools.domain.values import SchoolDTO


class ISchoolRepo(Protocol):
    def create_school(self, owner_id: int, school_name: str, city: str) -> None:
        """
        학교를 생성한다.
        """
        ...

    def search_schools(self, cmd: SearchSchoolsCmd) -> list[SchoolDTO]:
        """
        학교 목록을 반환한다. id 기준 오름차순으로 정렬한다.
        """
        ...

    def create_school_news(self, school_id: int, content: str) -> None:
        """
        학교 소식을 생성한다.
        """
        ...

    def list_schools(self, user_id: int) -> list[SchoolDTO]:
        """
        유저가 소유한 학교 목록을 반환한다.
        """
        ...

    def list_school_news(self, school_id: int) -> list[SchoolNewsEntity]:
        """
        학교 소식을 최신순으로 반환한다.
        """
        ...

    def update_school_news(self, news_id: int, content: str) -> SchoolNewsEntity:
        """
        학교 소식의 내용을 수정한다.
        """
        ...

    def delete_school_news(self, news_id: int) -> None:
        """
        학교 소식을 삭제한다.
        """
        ...

    def is_owned_news(self, owner_id: int, news_id: int) -> bool:
        """
        학교 소식이 유저의 것인지 확인한다.
        """
        ...

    def is_owned_school(self, owner_id: int, school_id: int) -> bool:
        """
        학교가 유저의 것인지 확인한다.
        """
        ...
