import pytest

from schools.models import Schools
from schools.tests.factories import SchoolFactory
from subscriptions.domain.entities import SubscriptionEntity
from subscriptions.models import Subscriptions
from subscriptions.tests.factories import SubscriptionFactory
from users.models import Users
from users.tests.factories import UserFactory


@pytest.mark.django_db
def test_subscriptions_from_entity():
    # given
    user: Users = UserFactory()
    school: Schools = SchoolFactory(owner=user)
    entity = SubscriptionEntity(
        user_id=user.id,
        school_id=school.id,
        canceled_at=None,
    )

    # when
    subscription = Subscriptions.from_entity(entity)

    # then
    assert subscription.user.id == entity.user_id
    assert subscription.school.id == entity.school_id
    assert subscription.subscribed_at == entity.subscribed_at
    assert subscription.canceled_at == entity.canceled_at


@pytest.mark.django_db
def test_subscriptions_to_entity():
    # given
    user: Users = UserFactory()
    school: Schools = SchoolFactory(owner=user)
    subscription: Subscriptions = SubscriptionFactory(user=user, school=school)

    # when
    entity = subscription.to_entity()

    # then
    assert entity.id == subscription.id
    assert entity.user_id == subscription.user.id
    assert entity.school_id == subscription.school.id
    assert entity.subscribed_at == subscription.subscribed_at
    assert entity.canceled_at == subscription.canceled_at
