from datetime import datetime, timedelta, timezone

import pytest
from freezegun import freeze_time

from schools.models import Schools
from schools.tests.factories import SchoolFactory, SchoolNewsFactory
from subscriptions.adapters.repos.subscriptions_repo import DjangoOrmSubscriptionsRepo
from subscriptions.domain.exceptions import (
    SubscriptionCancelFailed,
    SubscriptionCreateFailed,
)
from subscriptions.models import Subscriptions
from subscriptions.tests.factories import SubscriptionFactory
from users.domain.exceptions import UserNotFound
from users.models import Users
from users.tests.factories import UserFactory


@pytest.fixture
def school() -> Schools:
    owner = UserFactory()
    return SchoolFactory(owner=owner)


@pytest.fixture
def subscriber() -> Users:
    return UserFactory()


@pytest.fixture
def subscription_repo() -> DjangoOrmSubscriptionsRepo:
    return DjangoOrmSubscriptionsRepo()


@pytest.mark.django_db
def test_django_subscription_repo_first_subscribe(school, subscriber, subscription_repo):
    """
    최초 구독시 Subscription이 생성된다.
    """
    with freeze_time("2024-01-01 00:00:00"):
        # given
        subscribed_at = datetime.now(tz=timezone.utc)

        # when
        subscription_repo.create_subscription(user_id=subscriber.id, school_id=school.id)

        # then
        subscription = Subscriptions.objects.get(user_id=subscriber.id, school_id=school.id)
        assert subscription.user_id == subscriber.id
        assert subscription.school_id == school.id
        assert subscription.subscribed_at == subscribed_at
        assert subscription.canceled_at is None


@pytest.mark.django_db
def test_django_subscription_repo_reactivate_subscribe(school, subscriber, subscription_repo):
    """
    구독 취소 후 재구독시 Subscription이 업데이트된다.
    """
    with freeze_time("2024-01-01 00:00:00") as frozen_datetime:
        # given
        SubscriptionFactory(
            user=subscriber,
            school=school,
            subscribed_at=datetime.now(tz=timezone.utc),
            canceled_at=datetime.now(tz=timezone.utc) + timedelta(hours=1),
        )

        # when
        """
        구독 취소 후 재구독시 Subscription이 업데이트된다. 1일 이후 재구독한 상황을 가정하고 테스트를 작성했다.
        """
        frozen_datetime.tick(delta=timedelta(days=1))
        subscribed_at = datetime.now(tz=timezone.utc)

        subscription_repo.create_subscription(user_id=subscriber.id, school_id=school.id)

        # then
        subscription = Subscriptions.objects.get(user_id=subscriber.id, school_id=school.id)
        assert subscription.user_id == subscriber.id
        assert subscription.school_id == school.id
        assert subscription.subscribed_at == subscribed_at
        assert subscription.canceled_at is None


@pytest.mark.django_db
def test_django_subscription_repo_already_subscribed(school, subscriber, subscription_repo):
    """
    이미 구독한 경우 SubscriptionCreateFailed 예외가 발생한다.
    """
    # given
    SubscriptionFactory(user=subscriber, school=school)

    # when, then
    with pytest.raises(SubscriptionCreateFailed) as e:
        subscription_repo.create_subscription(user_id=subscriber.id, school_id=school.id)
    assert e.value.detail == "Already subscribed"


@pytest.mark.django_db
def test_django_subscription_repo_list_subscription(school, subscriber, subscription_repo):
    """
    구독중인 학교 목록을 조회할 수 있는지 확인한다.
    """
    # given
    SubscriptionFactory(user=subscriber, school=school)

    # when
    subscriptions = subscription_repo.list_subscription(user_id=subscriber.id)

    # then
    assert len(subscriptions) == 1
    assert subscriptions[0].user_id == subscriber.id
    assert subscriptions[0].school_id == school.id


@pytest.mark.django_db
def test_django_subscription_repo_cancel_subscription(school, subscriber, subscription_repo):
    """
    구독을 기대한대로 취소하는지 테스트한다.
    """
    with freeze_time("2024-01-01 00:00:00") as frozen_datetime:
        # given
        subscribed_at = datetime.now(tz=timezone.utc)
        SubscriptionFactory(user=subscriber, school=school, subscribed_at=subscribed_at)

        # when
        frozen_datetime.tick(delta=timedelta(days=1))
        canceled_at = datetime.now(tz=timezone.utc)
        subscription_repo.cancel_subscription(user_id=subscriber.id, school_id=school.id)

        # then
        subscription = Subscriptions.objects.get(user_id=subscriber.id, school_id=school.id)
        assert subscription.user_id == subscriber.id
        assert subscription.school_id == school.id
        assert subscription.subscribed_at == subscribed_at
        assert subscription.canceled_at == canceled_at


@pytest.mark.django_db
def test_django_subscription_repo_cancel_no_first_subscription(school, subscriber, subscription_repo):
    """
    한번도 구독한적이 없는 경우, SubscriptionCreateFailed 예외가 발생한다.
    """
    # when, then
    with pytest.raises(SubscriptionCancelFailed) as e:
        subscription_repo.cancel_subscription(user_id=subscriber.id, school_id=school.id)
    assert e.value.detail == "Subscription not found"


@pytest.mark.django_db
def test_django_subscription_repo_cancel_already_canceled(school, subscriber, subscription_repo):
    """
    이미 취소한 경우, SubscriptionCancelFailed 예외가 발생한다.
    """
    # given
    SubscriptionFactory(user=subscriber, school=school, canceled_at=datetime.now(tz=timezone.utc))

    # when, then
    with pytest.raises(SubscriptionCancelFailed) as e:
        subscription_repo.cancel_subscription(user_id=subscriber.id, school_id=school.id)
    assert e.value.detail == "Already canceled"


@pytest.mark.django_db
def test_iter_subscribed_schools_news(school, subscriber, subscription_repo):
    """
    구독한 학교들의 소식을 최신순으로 가져온다.
    소식은 구독을 시작한 시점 ~ 취소한 시점까지만 가져와야 한다. (단, 구독 시작 및 취소 시점과 동시에 생성된 소식은 포함 한다.)
    """
    with freeze_time("2024-01-01 00:00:00") as frozen_datetime:
        # given
        # 구독 이전 시점
        SchoolNewsFactory(school=school, created_at=datetime.now(tz=timezone.utc))  # 구독 이전 소식
        # 구독 시점
        frozen_datetime.tick(delta=timedelta(days=1))
        subscription = SubscriptionFactory(user=subscriber, school=school, subscribed_at=datetime.now(tz=timezone.utc))
        news1 = SchoolNewsFactory(school=school, created_at=datetime.now(tz=timezone.utc))  # 구독과 동시에 소식 생성
        # 구독 취소 시점
        frozen_datetime.tick(delta=timedelta(days=1))
        subscription.canceled_at = datetime.now(tz=timezone.utc)
        subscription.save()
        news2 = SchoolNewsFactory(school=school, created_at=datetime.now(tz=timezone.utc))  # 구독 취소와 동시에 소식 생성
        # 구독 취소 이후 글 생성
        frozen_datetime.tick(delta=timedelta(days=1))
        SchoolNewsFactory(school=school, created_at=datetime.now(tz=timezone.utc))  # 구독 취소 이후 소식

        # when
        page_cnt, news = subscription_repo.iter_subscribed_schools_news(
            user_id=subscriber.id, page_index=1, page_size=10
        )
        news = list(news)

        # then
        assert page_cnt == 1
        assert len(news) == 2
        assert [x.id for x in news] == [news2.id, news1.id]  # 최신순 반환 여부 테스트


@pytest.mark.django_db
def test_iter_subscribed_school_news_user_not_found(subscription_repo):
    """
    유저를 찾을 수 없는 경우, SubscriptionCreateFailed 예외가 발생한다.
    """
    # when, then
    with pytest.raises(UserNotFound):
        subscription_repo.iter_subscribed_schools_news(user_id=9999, page_index=1, page_size=10)
