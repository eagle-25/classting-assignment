from schools.domain.entities import SchoolNewsEntity
from subscriptions.domain.entities import SubscriptionEntity
from subscriptions.domain.interfaces import ISubscriptionsRepo


def create_subscription_usecase(subscription_repo: ISubscriptionsRepo, user_id: int, school_id: int) -> None:
    """
    구독을 생성하는 유스케이스
    """
    subscription_repo.create_subscription(user_id=user_id, school_id=school_id)


def list_subscription_usecase(subscription_repo: ISubscriptionsRepo, user_id: int) -> list[SubscriptionEntity]:
    """
    구독한 학교 목록을 조회하는 유스케이스
    """
    return subscription_repo.list_subscriptions(user_id=user_id)


def delete_subscription_usecase(subscription_repo: ISubscriptionsRepo, user_id: int, school_id: int) -> None:
    """
    구독한 학교를 삭제하는 유스케이스
    """
    subscription_repo.cancel_subscription(user_id=user_id, school_id=school_id)


def list_subscribed_schools_news_usecase(
    subscription_repo: ISubscriptionsRepo, user_id: int, page_index: int = 1
) -> list[SchoolNewsEntity]:
    """
    구독한 학교들의 소식을 가져오는 유스케이스
    """
    PAGE_SIZE = 10
    page_cnt, news = subscription_repo.iter_subscribed_schools_news(
        user_id=user_id, page_index=page_index, page_size=PAGE_SIZE
    )
    return list(news)
