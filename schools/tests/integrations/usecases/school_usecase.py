import pytest

from schools.adapters.repos.django_school_repo import DjangoOrmSchoolsRepo
from schools.models import Schools
from schools.tests.factories import SchoolFactory
from schools.usecases.school_usecase import create_school_usecase, list_schools_usecase
from users.tests.factories import UserFactory


@pytest.mark.django_db
def test_list_schools_usecase():
    """
    owner가 가지는 학교들을 조회할 수 있는지 테스트
    """
    # given
    user = UserFactory()
    school1 = SchoolFactory(owner_id=user.id)
    school2 = SchoolFactory(owner_id=user.id)

    # when
    schools = list_schools_usecase(school_repo=DjangoOrmSchoolsRepo(), owner_id=user.id)

    # then
    assert len(schools) == 2
    assert schools[0] == school1.to_entity()
    assert schools[1] == school2.to_entity()


def test_create_schools_usecase():
    """
    학교를 생성할 수 있는지 테스트
    """
    # given
    user = UserFactory()
    name = "school"
    city = "city"

    # when
    create_school_usecase(school_repo=DjangoOrmSchoolsRepo(), owner_id=user.id, name=name, city=city)

    # then
    assert Schools.objects.filter(owner_id=user.id, name=name, city=city).exists()
