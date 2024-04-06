from common.exceptions import InvalidParameter, ValidationFailed
from subscriptions.domain.interfaces import ISubscriptionRepo
from users.domain.values import UserType
from users.models import Users


def _validate_is_expected_user(user_id: int, expected_user_type: UserType):
    try:
        user = Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        raise ValidationFailed(detail=f"User not found: id={user_id}")
    if user.user_type != expected_user_type:
        raise ValidationFailed(detail=f"User:{user_id} should be {expected_user_type.value}")
    return user


def create_subscription_usecase(subscription_repo: ISubscriptionRepo, subscriber_id: int, publisher_id: int):
    if subscriber_id == publisher_id:
        raise InvalidParameter(detail="Cannot subscribe same user")
    else:
        _validate_is_expected_user(user_id=subscriber_id, expected_user_type=UserType.SUBSCRIBER)
        _validate_is_expected_user(user_id=publisher_id, expected_user_type=UserType.PUBLISHER)

    subscription_repo.create_subscription(subscriber_id=subscriber_id, publisher_id=publisher_id)


def delete_subscription_usecase(subscription_repo: ISubscriptionRepo, subscriber_id: int, publisher_id: int):
    if subscriber_id == publisher_id:
        raise InvalidParameter(detail="Cannot subscribe same user")
    else:
        _validate_is_expected_user(user_id=subscriber_id, expected_user_type=UserType.SUBSCRIBER)
        _validate_is_expected_user(user_id=publisher_id, expected_user_type=UserType.PUBLISHER)
    subscription_repo.delete_subscription(subscriber_id=subscriber_id, publisher_id=publisher_id)


def get_publisher_ids_usecase(subscription_repo: ISubscriptionRepo, subscriber_id: int) -> list[int]:
    _validate_is_expected_user(user_id=subscriber_id, expected_user_type=UserType.SUBSCRIBER)
    return list(subscription_repo.get_publisher_ids(subscriber_id=subscriber_id))
