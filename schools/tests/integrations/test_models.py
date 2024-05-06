import pytest

from schools.domain.entities import SchoolEntity, SchoolNewsEntity
from schools.models import SchoolNews, Schools
from schools.tests.factories import SchoolFactory, SchoolNewsFactory
from users.adapter.outcome.persistence.models import Users
from users.tests.factories import UserFactory


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


@pytest.mark.django_db
def test_school_news_to_entity():
    # given
    user: Users = UserFactory()
    school: Schools = SchoolFactory(owner_id=user.id)
    school_news: SchoolNews = SchoolNewsFactory(school_id=school.id)

    # when
    res = school_news.to_entity()

    # then
    assert isinstance(res, SchoolNewsEntity)
    assert res.id == school_news.id
    assert res.school_id == school_news.school.id
    assert res.content == school_news.content
    assert res.created_at == school_news.created_at
    assert res.updated_at == school_news.updated_at
