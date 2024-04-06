import pytest

from users.domain.entities import UserEntity
from users.models import Users
from users.tests.factories import UsersFactory


@pytest.mark.django_db
def test_users_to_entity():
    # given
    user = UsersFactory()
    # when
    entity = user.to_entity()
    # then
    assert isinstance(entity, UserEntity)
    assert entity.id == user.id
    assert entity.email == user.email
    assert entity.password == user.password


def test_users_from_entity():
    # given
    entity = UserEntity(id=1, email="email", password="password")
    # when
    user = Users.from_entity(entity)
    # then
    assert isinstance(user, Users)
    assert user.id == entity.id
    assert user.email == entity.email
    assert user.password == entity.password
