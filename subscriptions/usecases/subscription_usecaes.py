from common.exceptions import InvalidParameter, ValidationFailed
from subscriptions.domain.interfaces import ISubscriptionRepo
from users.domain.interfaces import IUserRepo
from users.domain.values import UserType


def _validate_user(user_repo: IUserRepo, user_id: int, expected_user_type: UserType):
    user = user_repo.get(user_id=user_id)
    if user is None:
        raise ValidationFailed(detail="User not found")
    if user.user_type != expected_user_type:
        raise InvalidParameter(detail=f"User should be {expected_user_type.value}")


def _validate_subscriber_and_publisher(user_repo: IUserRepo, subscriber_id: int, publisher_id: int) -> None:
    if subscriber_id == publisher_id:
        raise InvalidParameter(detail="Cannot subscribe same user")
    _validate_user(user_repo=user_repo, user_id=subscriber_id, expected_user_type=UserType.SUBSCRIBER)
    _validate_user(user_repo=user_repo, user_id=publisher_id, expected_user_type=UserType.PUBLISHER)


class CreateSubscriptionUsecase:
    def __init__(self, subscription_repo: ISubscriptionRepo, user_repo: IUserRepo) -> None:
        self.subscription_repo = subscription_repo
        self.user_repo = user_repo

    def execute(self, subscriber_id: int, publisher_id: int):
        _validate_subscriber_and_publisher(
            user_repo=self.user_repo, subscriber_id=subscriber_id, publisher_id=publisher_id
        )
        self.subscription_repo.create(subscriber_id=subscriber_id, publisher_id=publisher_id)


class DeleteSubscriptionUsecase:
    def __init__(self, subscription_repo: ISubscriptionRepo, user_repo: IUserRepo) -> None:
        self.subscription_repo = subscription_repo
        self.user_repo = user_repo

    def execute(self, subscriber_id: int, publisher_id: int):
        _validate_subscriber_and_publisher(
            user_repo=self.user_repo, subscriber_id=subscriber_id, publisher_id=publisher_id
        )
        self.subscription_repo.delete(subscriber_id=subscriber_id, publisher_id=publisher_id)


class GetPublisherIdsUsecase:
    def __init__(self, subscription_repo: ISubscriptionRepo, user_repo: IUserRepo) -> None:
        self.subscription_repo = subscription_repo
        self.user_repo = user_repo

    def execute(self, subscriber_id: int) -> list[int]:
        _validate_user(user_repo=self.user_repo, user_id=subscriber_id, expected_user_type=UserType.SUBSCRIBER)
        return list(self.subscription_repo.get_publisher_ids(subscriber_id=subscriber_id))
