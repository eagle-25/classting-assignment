import pytest

from users.domain.entities import UserEntity
from users.tests.factories import UserFactory


@pytest.mark.django_db
def test_users_to_entity():
    # given
    user = UserFactory()
    # when
    entity = user.to_entity()
    # then
    assert isinstance(entity, UserEntity)
    assert entity.id == user.id
    assert entity.email == user.email
    assert entity.password == user.password
