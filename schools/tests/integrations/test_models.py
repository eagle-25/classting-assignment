import pytest

from schools.domain.entities import SchoolEntity
from schools.models import Schools
from schools.tests.factories import SchoolFactory
from users.tests.factories import UserFactory


@pytest.mark.django_db
def test_school_from_entity():
    # given
    user = UserFactory()
    entity = SchoolEntity(
        owner_id=user.id,
        name="classting",
        city="seoul",
    )

    # when
    res = Schools.from_entity(entity=entity)

    # then
    assert isinstance(res, Schools)
    assert res.owner_id == entity.owner_id
    assert res.name == entity.name
    assert res.city == entity.city


@pytest.mark.django_db
def test_school_to_entity():
    # given
    user = UserFactory()
    schools: Schools = SchoolFactory(owner_id=user.id)

    # when
    res = schools.to_entity()

    # then
    assert isinstance(res, SchoolEntity)
    assert res.id == schools.id
    assert res.owner_id == schools.owner.id
    assert res.name == schools.name
    assert res.city == schools.city
    assert res.created_at == schools.created_at
