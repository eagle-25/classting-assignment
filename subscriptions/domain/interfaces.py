from collections.abc import Iterator
from typing import Protocol


class ISubscriptionRepo(Protocol):
    def create(self, subscriber_id: int, publisher_id: int) -> None:
        ...

    def delete(self, subscriber_id: int, publisher_id: int) -> None:
        ...

    def get_publisher_ids(self, subscriber_id: int) -> Iterator[int]:
        ...
