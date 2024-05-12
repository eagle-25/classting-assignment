from datetime import datetime

import pytest
from faker import Faker

from users.domain.user_entity import UserEntity

_faker = Faker()


@pytest.fixture
def user() -> UserEntity:
    return UserEntity(
        id=_faker.random_int(),
        email=_faker.email(),
        password=_faker.password(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
