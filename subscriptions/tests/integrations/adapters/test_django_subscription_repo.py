import pytest

from subscriptions.adapters.repos.django_subscription_repo import (
    DjangoOrmSubscriptionRepo,
)
from subscriptions.domain.exceptions import (
    SubscriptionCreateFailed,
    SubscriptionNotFound,
)
from subscriptions.models import Subscriptions
from subscriptions.tests.factories import SubscriptionsFactory
from users.domain.values import UserType
from users.tests.factories import UsersFactory


@pytest.fixture
def subscriber():
    return UsersFactory(user_type=UserType.SUBSCRIBER)


@pytest.fixture
def publisher():
    return UsersFactory(user_type=UserType.PUBLISHER)


@pytest.mark.django_db
def test_django_subscription_repo_create_new(subscriber, publisher):
    """
    새로운 Subscription 생성이 정상적으로 이루어지는지 테스트
    """
    # when
    repo = DjangoOrmSubscriptionRepo()
    repo.create(subscriber_id=subscriber.id, publisher_id=publisher.id)

    # then
    subscriptions = Subscriptions.objects.filter(subscriber_id=subscriber.id, publisher_id=publisher.id)
    assert subscriptions.count() == 1
    assert subscriptions[0].is_deleted is False
    assert subscriptions[0].deleted_at is None


@pytest.mark.django_db
def test_django_subscription_repo_resubscribe(subscriber, publisher):
    """
    이미 삭제된 Subscription을 재구독하는 경우, Subscription이 활성화되어야 한다.
    """
    # given
    SubscriptionsFactory(subscriber=subscriber, publisher=publisher, is_deleted=True)

    # when
    repo = DjangoOrmSubscriptionRepo()
    repo.create(subscriber_id=subscriber.id, publisher_id=publisher.id)

    # then
    subscription = Subscriptions.objects.get(subscriber_id=subscriber.id, publisher_id=publisher.id)
    assert subscription.is_deleted is False
    assert subscription.deleted_at is None


@pytest.mark.django_db
def test_djagno_subscription_repo_duplicated_error(subscriber, publisher):
    """
    이미 활성화된 subscription이 있는 상태에서 새로운 subscription을 생성하려고 하면 SubscriptionDuplicatedError가 발생해야 한다.
    """
    # given
    SubscriptionsFactory(subscriber=subscriber, publisher=publisher, is_deleted=False)

    # when
    with pytest.raises(SubscriptionCreateFailed):
        repo = DjangoOrmSubscriptionRepo()
        repo.create(subscriber.id, publisher.id)


@pytest.mark.django_db
def test_django_subscription_repo_delete(subscriber, publisher):
    """
    Subscription 삭제가 정상적으로 이루어지는지 테스트 한다.
    """
    # given
    SubscriptionsFactory(subscriber=subscriber, publisher=publisher, is_deleted=False)

    # when
    repo = DjangoOrmSubscriptionRepo()
    repo.delete(subscriber.id, publisher.id)

    # then
    subscription = Subscriptions.objects.get(subscriber_id=subscriber.id, publisher_id=publisher.id)
    assert subscription.is_deleted is True
    assert subscription.deleted_at is not None


@pytest.mark.django_db
def test_django_subscription_repo_delete_not_found(subscriber, publisher):
    """
    존재하지 않는 Subscription을 삭제하려고 할 때 SubscriptionNotFound가 발생해야 한다.
    """
    # given
    SubscriptionsFactory(subscriber=subscriber, publisher=publisher, is_deleted=True)

    # when, then
    with pytest.raises(SubscriptionNotFound) as e:
        repo = DjangoOrmSubscriptionRepo()
        repo.delete(subscriber.id, publisher.id)
    assert e.value.detail == f"subscriber_id: {subscriber.id}, publisher_id: {publisher.id}"


@pytest.mark.django_db
def test_django_subscription_repo_get_publisher_ids(subscriber):
    """
    구독자가 구독 중인 publisher_id 리스트를 반환하는지 테스트한다.
    """
    # given
    publisher_1 = UsersFactory(user_type=UserType.PUBLISHER)
    SubscriptionsFactory(subscriber=subscriber, publisher=publisher_1, is_deleted=False)

    publisher_2 = UsersFactory(user_type=UserType.PUBLISHER)
    SubscriptionsFactory(subscriber=subscriber, publisher=publisher_2, is_deleted=False)

    # when
    repo = DjangoOrmSubscriptionRepo()
    res = repo.get_publisher_ids(subscriber.id)

    # then
    assert list(res) == [publisher_1.id, publisher_2.id]
