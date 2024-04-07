from collections.abc import Iterable
from typing import Protocol

from schools.domain.entities import SchoolNewsEntity
from subscriptions.domain.entities import SubscriptionEntity


class ISubscriptionsRepo(Protocol):
    def create_subscription(self, user_id: int, school_id: int) -> None:
        """
        구독을 생성한다.
        """
        pass

    def list_subscription(self, user_id: int) -> list[SubscriptionEntity]:
        """
        구독한 학교 목록을 조회한다.
        """
        pass

    def delete_subscription(self, user_id: int, school_id: int) -> None:
        """
        구독한 학교를 삭제한다.
        """
        pass

    def iter_subscribed_schools_news(
        self, user_id: int, page_index: int = 1, page_size: int = 10
    ) -> tuple[int, Iterable[SchoolNewsEntity]]:  # page_cnt, news
        """
        구독한 학교들의 소식을 최신순으로 가져온다. 소식이 많을 경우를 대비해 pagination을 지원한다.

        @param user_id: 구독을 조회할 유저의 id
        @param page_index: 조회할 페이지의 인덱스
        @param page_size: 한 페이지에서 보여줄 소식의 개수
        @return: (page_cnt, news) - page_cnt: 전체 페이지 수, news: 소식들
        """
        pass
