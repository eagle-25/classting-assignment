import pytest

from users.domain.entities import UserEntity
from users.domain.values import UserType
from users.models import Users
from users.tests.factories import UsersFactory


@pytest.mark.django_db
def test_users_to_entity():
    # given
    user = UsersFactory(user_type=UserType.PUBLISHER)
    # when
    entity = user.to_entity()
    # then
    assert entity.id == user.id
    assert entity.email == user.email
    assert entity.password == user.password
    assert entity.user_type == user.user_type


def test_users_from_entity():
    # given
    entity = UserEntity(
        id=1, email="email", password="password", user_type=UserType.PUBLISHER
    )
    # when
    user = Users.from_entity(entity)
    # then
    assert user.id == entity.id
    assert user.email == entity.email
    assert user.password == entity.password
    assert user.user_type == entity.user_type
