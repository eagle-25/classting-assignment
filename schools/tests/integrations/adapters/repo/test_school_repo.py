import pytest

from schools.adapters.repos.school_repo import DjangoOrmSchoolsRepo
from schools.domain.commands import ListSchoolsCmd
from schools.domain.exceptions import (
    SchoolCreateFailed,
    SchoolNewsNotFound,
    SchoolNotFound,
)
from schools.models import SchoolNews, Schools
from schools.tests.factories import SchoolFactory, SchoolNewsFactory
from users.models import Users
from users.tests.factories import UserFactory


@pytest.mark.django_db
def test_django_school_repo_list_schools():
    """
    owner가 가지는 학교들을 조회할 수 있는지 테스트
    """
    # given
    user: Users = UserFactory()
    school1: Schools = SchoolFactory(owner_id=user.id, city="Seoul", name="SNU")
    SchoolFactory(owner_id=user.id, city="Seoul", name="KU")
    SchoolFactory(owner_id=user.id, city="Busan", name="PNU")

    # when
    repo = DjangoOrmSchoolsRepo()
    cmd = ListSchoolsCmd(owner_id=user.id, city="Seoul", school_name="SNU")
    schools = repo.list_schools(cmd=cmd)

    # then
    assert len(schools) == 1
    assert schools[0] == school1.to_entity()


@pytest.mark.django_db
def test_django_school_repo_create_school():
    """
    학교를 생성할 수 있는지 테스트
    """
    # given
    user: Users = UserFactory()
    school = SchoolFactory.build(owner_id=user.id)

    # when
    repo = DjangoOrmSchoolsRepo()
    repo.create_school(entity=school)

    # then
    assert Schools.objects.filter(owner_id=user.id, name=school.name, city=school.city).exists()


@pytest.mark.django_db
def test_django_school_repo_create_school_failed():
    """
    이미 존재하는 학교를 생성하려고 할 때 실패하는지 테스트
    """
    # given
    user: Users = UserFactory()
    school = SchoolFactory(owner_id=user.id)

    # when, then
    repo = DjangoOrmSchoolsRepo()
    with pytest.raises(SchoolCreateFailed) as e:
        repo.create_school(entity=school)
    assert e.value.detail == "Already exists"


@pytest.mark.django_db
def test_django_school_repo_create_school_news():
    """
    학교 소식을 생성할 수 있는지 테스트
    """
    # given
    user = UserFactory()
    school = SchoolFactory(owner_id=user.id)
    school_news = SchoolNewsFactory(school_id=school.id)

    # when
    repo = DjangoOrmSchoolsRepo()
    repo.create_school_news(entity=school_news)

    # then
    assert Schools.objects.filter(id=school.id).exists()


@pytest.mark.django_db
def test_django_school_repo_list_school_news():
    """
    학교 소식을 조회할 수 있는지 테스트. 최신순으로 소식을 반환해야한다.
    """
    # given
    user = UserFactory()
    school = SchoolFactory(owner_id=user.id)
    school_news1 = SchoolNewsFactory(school_id=school.id)
    school_news2 = SchoolNewsFactory(school_id=school.id)

    # when
    repo = DjangoOrmSchoolsRepo()
    school_news = repo.list_school_news(school_id=school.id)

    # then
    assert len(school_news) == 2
    assert school_news[0] == school_news2.to_entity()
    assert school_news[1] == school_news1.to_entity()


@pytest.mark.django_db
def test_django_school_repo_update_school_news():
    """
    학교 소식을 수정할 수 있는지 테스트
    """
    # given
    user = UserFactory()
    school = SchoolFactory(owner_id=user.id)
    school_news = SchoolNewsFactory(school_id=school.id)
    content = "new content"

    # when
    repo = DjangoOrmSchoolsRepo()
    res = repo.update_school_news(news_id=school_news.id, content=content)

    # then
    news = SchoolNews.objects.get(id=school_news.id)
    assert news.content == content
    assert res == news.to_entity()


@pytest.mark.django_db
def tset_djagno_school_repo_update_school_news_not_found():
    """
    존재하지 않는 소식을 수정할 때 에러가 발생하는지 테스트
    """
    # when, then
    repo = DjangoOrmSchoolsRepo()
    with pytest.raises(SchoolNotFound):
        repo.update_school_news(news_id=1, content="content")


@pytest.mark.django_db
def test_django_school_repo_delete_school_news():
    """
    학교 소식을 삭제할 수 있는지 테스트
    """
    # given
    user = UserFactory()
    school = SchoolFactory(owner_id=user.id)
    school_news = SchoolNewsFactory(school_id=school.id)

    # when
    repo = DjangoOrmSchoolsRepo()
    repo.delete_school_news(news_id=school_news.id)

    # then
    assert not SchoolNews.objects.filter(id=school_news.id).exists()


@pytest.mark.django_db
def test_django_school_repo_delete_school_news_not_found():
    """
    존재하지 않는 소식을 삭제할 때 에러가 발생하는지 테스트
    """
    # when, then
    repo = DjangoOrmSchoolsRepo()
    with pytest.raises(SchoolNotFound):
        repo.delete_school_news(news_id=1)


@pytest.mark.django_db
def test_django_school_repo_is_owned_news():
    """
    소식이 소유자의 것인지 확인할 수 있는지 테스트
    """
    # given
    owner = UserFactory()
    school = SchoolFactory(owner_id=owner.id)
    school_news = SchoolNewsFactory(school_id=school.id)

    # when, then
    repo = DjangoOrmSchoolsRepo()
    assert repo.is_owned_news(owner_id=owner.id, news_id=school_news.id)
    assert not repo.is_owned_news(owner_id=owner.id + 1, news_id=school_news.id)


@pytest.mark.django_db
def test_django_school_repo_is_owned_news_no_news():
    """
    존재하지 않는 소식을 조회할 때 에러가 발생하는지 테스트
    """
    # given
    user = UserFactory()

    # when, then
    repo = DjangoOrmSchoolsRepo()
    with pytest.raises(SchoolNewsNotFound):
        repo.is_owned_news(owner_id=user.id, news_id=1)


@pytest.mark.django_db
def test_django_school_repo_is_owned_school():
    """
    학교가 소유자의 것인지 확인할 수 있는지 테스트
    """
    # given
    user = UserFactory()
    school = SchoolFactory(owner_id=user.id)

    # when, then
    repo = DjangoOrmSchoolsRepo()
    assert repo.is_owned_school(owner_id=user.id, school_id=school.id)
    assert not repo.is_owned_school(owner_id=user.id + 1, school_id=school.id)


@pytest.mark.django_db
def test_django_school_repo_is_owned_school_no_school():
    """
    존재하지 않는 학교를 조회할 때 에러가 발생하는지 테스트
    """
    # given
    user = UserFactory()

    # when, then
    repo = DjangoOrmSchoolsRepo()
    with pytest.raises(SchoolNotFound):
        repo.is_owned_school(owner_id=user.id, school_id=1)
