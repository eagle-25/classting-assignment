import pytest

from subscriptions.domain.entities import SubscriptionEntity
from subscriptions.models import Subscriptions
from subscriptions.tests.factories import SubscriptionsFactory
from users.domain.values import UserType
from users.models import Users
from users.tests.factories import UsersFactory


@pytest.mark.django_db
def test_subscriptions_from_entity():
    # given
    publisher: Users = UsersFactory(user_type=UserType.PUBLISHER)
    subscriber: Users = UsersFactory(user_type=UserType.SUBSCRIBER)

    entity = SubscriptionEntity(
        id=1,
        publisher_id=publisher.id,
        subscriber_id=subscriber.id,
        is_deleted=False,
        deleted_at=None,
    )

    # when
    res = Subscriptions.from_entity(entity)

    # then
    assert isinstance(res, Subscriptions)
    assert res.id == entity.id
    assert res.publisher_id == entity.publisher_id
    assert res.subscriber_id == entity.subscriber_id
    assert res.is_deleted == entity.is_deleted


@pytest.mark.django_db
def test_subscriptions_to_entity():
    # given
    subscription: Subscriptions = SubscriptionsFactory()

    # when
    res = subscription.to_entity()

    # then
    assert isinstance(res, SubscriptionEntity)
    assert res.id == subscription.id
    assert res.publisher_id == subscription.publisher.id
    assert res.subscriber_id == subscription.subscriber.id
    assert res.is_deleted == subscription.is_deleted
    assert res.deleted_at == subscription.deleted_at
