import pytest

from common.exceptions import InvalidParameter
from subscriptions.adapters.repos.django_subscription_repo import (
    DjangoOrmSubscriptionRepo,
)
from subscriptions.models import Subscriptions
from subscriptions.tests.factories import SubscriptionsFactory
from subscriptions.usecases.subscription_usecaes import (
    CreateSubscriptionUsecase,
    DeleteSubscriptionUsecase,
    GetPublisherIdsUsecase,
    _validate_subscriber_and_publisher,
    _validate_user,
)
from users.adapters.repos.django_user_repo import DjangoOrmUserRepo
from users.domain.exceptions import UserNotFound
from users.domain.values import UserType
from users.models import Users
from users.tests.factories import UsersFactory


@pytest.fixture
def subscriber() -> Users:
    return UsersFactory(user_type=UserType.SUBSCRIBER)


@pytest.fixture
def publisher() -> Users:
    return UsersFactory(user_type=UserType.PUBLISHER)


@pytest.mark.django_db
def test_validate_user_not_found():
    """
    유저가 존재하지 않을 경우 ValidationFailed 예외가 발생한다.
    """
    # when
    with pytest.raises(UserNotFound) as e:
        _validate_user(user_repo=DjangoOrmUserRepo(), user_id=1, expected_user_type=UserType.SUBSCRIBER)
    assert e.value.detail == "User not found"


@pytest.mark.django_db
def test_validate_user_not_expected_type():
    """
    기대한 유저 type이 아닐 경우 InvalidParameter 예외가 발생한다.
    """
    # given
    user = UsersFactory(user_type=UserType.SUBSCRIBER)

    # when
    _validate_user(user_repo=DjangoOrmUserRepo(), user_id=user.id, expected_user_type=UserType.SUBSCRIBER)


@pytest.mark.django_db
def test_validate_subscriber_and_publisher_same_error():
    """
    subscriber와 publisher가 같은 경우 InvalidParameter 예외가 발생한다.
    """
    # given
    user = UsersFactory(user_type=UserType.SUBSCRIBER)

    # when
    with pytest.raises(InvalidParameter) as e:
        _validate_subscriber_and_publisher(user_repo=DjangoOrmUserRepo(), subscriber_id=user.id, publisher_id=user.id)
    assert e.value.detail == "Cannot subscribe same user"


@pytest.mark.django_db
def test_validate_subscriber_and_publisher_not_subscriber():
    """
    subscriber가 아닌 경우 InvalidParameter 예외가 발생한다.
    """
    # given
    subscriber = UsersFactory(user_type=UserType.PUBLISHER)
    publisher = UsersFactory(user_type=UserType.PUBLISHER)

    # when
    with pytest.raises(InvalidParameter) as e:
        _validate_subscriber_and_publisher(
            user_repo=DjangoOrmUserRepo(), subscriber_id=subscriber.id, publisher_id=publisher.id
        )
    assert e.value.detail == "User should be subscriber"


@pytest.mark.django_db
def test_validate_subscriber_and_publisher_not_publisher():
    """
    publisher가 아닌 경우 InvalidParameter 예외가 발생한다.
    """
    # given
    subscriber = UsersFactory(user_type=UserType.SUBSCRIBER)
    publisher = UsersFactory(user_type=UserType.SUBSCRIBER)

    # when
    with pytest.raises(InvalidParameter) as e:
        _validate_subscriber_and_publisher(
            user_repo=DjangoOrmUserRepo(), subscriber_id=subscriber.id, publisher_id=publisher.id
        )
    assert e.value.detail == "User should be publisher"


@pytest.mark.django_db
def test_create_subscription_usecase(subscriber, publisher):
    """
    구독 생성이 정상적으로 동작하는지 테스트한다.
    """
    # when
    usecase = CreateSubscriptionUsecase(
        subscription_repo=DjangoOrmSubscriptionRepo(),
        user_repo=DjangoOrmUserRepo(),
    )
    usecase.execute(subscriber_id=subscriber.id, publisher_id=publisher.id)

    # then
    assert Subscriptions.objects.filter(
        subscriber_id=subscriber.id, publisher_id=publisher.id, is_deleted=False
    ).exists()


@pytest.mark.django_db
def test_get_publisher_ids_usecase(subscriber, publisher):
    """
    구독 조회 usecase가 정상적으로 동작하는지 테스트한다.
    """
    # given
    SubscriptionsFactory(subscriber=subscriber, publisher=publisher)

    usecase = GetPublisherIdsUsecase(
        subscription_repo=DjangoOrmSubscriptionRepo(),
        user_repo=DjangoOrmUserRepo(),
    )

    # when
    res = usecase.execute(subscriber_id=subscriber.id)

    # then
    assert res == [publisher.id]


@pytest.mark.django_db
def test_delete_subscription_usecase(subscriber, publisher):
    """
    구독 삭제 usecase가 정상적으로 동작하는지 테스트한다.
    """
    # given
    subscription = SubscriptionsFactory(subscriber=subscriber, publisher=publisher)

    usecase = DeleteSubscriptionUsecase(
        subscription_repo=DjangoOrmSubscriptionRepo(),
        user_repo=DjangoOrmUserRepo(),
    )

    # when
    usecase.execute(subscriber_id=subscriber.id, publisher_id=publisher.id)

    # then
    assert Subscriptions.objects.filter(id=subscription.id, is_deleted=True).exists()
