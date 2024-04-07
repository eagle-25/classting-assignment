import pytest

from schools.tests.factories import SchoolFactory, SchoolNewsFactory
from subscriptions.adapters.repos.subscriptions_repo import DjangoOrmSubscriptionsRepo
from subscriptions.models import Subscriptions
from subscriptions.tests.factories import SubscriptionFactory
from users.tests.factories import UserFactory


@pytest.mark.django_db
def test_create_subscription_usecase() -> None:
    """
    구독을 생성하는 유스케이스 테스트
    """
    # Given
    school = SchoolFactory(owner=UserFactory())
    subscriber = UserFactory()

    # When
    repo = DjangoOrmSubscriptionsRepo()
    repo.create_subscription(user_id=subscriber.id, school_id=school.id)

    # Then
    subscriptions = Subscriptions.objects.filter(user_id=subscriber.id, school_id=school.id, canceled_at__isnull=True)
    assert len(subscriptions) == 1


@pytest.mark.django_db
def test_cancel_subscription_usecase() -> None:
    """
    구독을 취소하는 유스케이스 테스트
    """
    # Given
    school = SchoolFactory(owner=UserFactory())
    subscriber = UserFactory()
    SubscriptionFactory(user=subscriber, school=school)

    # When
    repo = DjangoOrmSubscriptionsRepo()
    repo.delete_subscription(user_id=subscriber.id, school_id=school.id)

    # Then
    subscriptions = Subscriptions.objects.filter(user_id=subscriber.id, school_id=school.id, canceled_at__isnull=False)
    assert len(subscriptions) == 0


@pytest.mark.django_db
def test_list_subscribed_schools_usecase():
    """
    구독한 학교 목록을 가져오는 유스케이스 테스트
    """
    # Given
    school = SchoolFactory(owner=UserFactory())
    subscriber = UserFactory()
    SubscriptionFactory(user=subscriber, school=school)

    # When
    repo = DjangoOrmSubscriptionsRepo()
    res = repo.list_subscription(user_id=subscriber.id)

    # Then
    assert len(res) == 1
    assert res[0].id == school.id


@pytest.mark.django_db
def test_list_subscribed_schools_news_usecase():
    """
    소식을 최신순으로 가져올 수 있는지 테스트
    """
    # Given
    school = SchoolFactory(owner=UserFactory())
    subscriber = UserFactory()
    SubscriptionFactory(user=subscriber, school=school)
    news_ids = [SchoolNewsFactory(school=school).id for _ in range(3)]

    # When
    repo = DjangoOrmSubscriptionsRepo()
    page_cnt, news = repo.iter_subscribed_schools_news(user_id=subscriber.id, page_index=1, page_size=10)

    # Then
    assert page_cnt == 1
    assert [x.id for x in list(news)] == news_ids[::-1]
