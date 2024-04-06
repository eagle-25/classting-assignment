import pytest

from schools.adapters.repos.django_school_repo import DjangoOrmSchoolsRepo
from schools.domain.exceptions import SchoolCreateFailed
from schools.models import Schools
from schools.tests.factories import SchoolFactory
from users.models import Users
from users.tests.factories import UserFactory


@pytest.mark.django_db
def test_django_school_repo_list():
    """
    owner가 가지는 학교들을 조회할 수 있는지 테스트
    """
    # given
    user: Users = UserFactory()
    school1: Schools = SchoolFactory(owner_id=user.id)
    school2: Schools = SchoolFactory(owner_id=user.id)

    # when
    repo = DjangoOrmSchoolsRepo()
    schools = repo.list(owner_id=user.id)

    # then
    assert len(schools) == 2
    assert schools[0] == school1.to_entity()
    assert schools[1] == school2.to_entity()


@pytest.mark.django_db
def test_django_school_repo_create():
    """
    학교를 생성할 수 있는지 테스트
    """
    # given
    user: Users = UserFactory()
    school = SchoolFactory.build(owner_id=user.id)

    # when
    repo = DjangoOrmSchoolsRepo()
    repo.create(entity=school)

    # then
    assert Schools.objects.filter(owner_id=user.id, name=school.name, city=school.city).exists()


@pytest.mark.django_db
def test_django_school_repo_create_failed():
    """
    이미 존재하는 학교를 생성하려고 할 때 실패하는지 테스트
    """
    # given
    user: Users = UserFactory()
    school = SchoolFactory(owner_id=user.id)

    # when, then
    repo = DjangoOrmSchoolsRepo()
    with pytest.raises(SchoolCreateFailed) as e:
        repo.create(entity=school)
    assert e.value.detail == "Already exists"
