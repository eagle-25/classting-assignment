import pytest

from common.exceptions import Unauthorized
from schools.adapters.repos.school_repo import DjangoOrmSchoolsRepo
from schools.models import SchoolNews, Schools
from schools.tests.factories import SchoolFactory, SchoolNewsFactory
from schools.usecases.school_usecase import (
    create_school_news_usecase,
    create_school_usecase,
    delete_school_news_usecase,
    list_school_news_usecase,
    list_schools_usecase,
    update_school_news_usecase,
)
from users.tests.factories import UserFactory


@pytest.mark.django_db
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


@pytest.mark.django_db
def test_list_schools_usecase():
    """
    owner_id에 해당하는 학교를 조회할 수 있는지 테스트. 반환되는 학교 id는 오름차순이어야 한다.
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


@pytest.mark.django_db
def test_create_school_news_usecase():
    """
    학교 소식을 생성할 수 있는지 테스트
    """
    # given
    user = UserFactory()
    school = SchoolFactory(owner_id=user.id)
    content = "content"

    # when
    repo = DjangoOrmSchoolsRepo()
    create_school_news_usecase(school_repo=repo, owner_id=user.id, school_id=school.id, content=content)

    # then
    assert SchoolNews.objects.filter(school_id=school.id, content=content).exists()


@pytest.mark.django_db
def create_school_news_usecase_with_not_owned_school():
    """
    소유하지 않은 학교에 소식을 생성할 수 없는지 테스트
    """
    # given
    owner = UserFactory()
    school = SchoolFactory(owner_id=owner.id)
    content = "content"

    # when
    not_owner = UserFactory()

    with pytest.raises(Unauthorized):
        repo = DjangoOrmSchoolsRepo()
        create_school_news_usecase(school_repo=repo, owner_id=not_owner.id, school_id=school.id, content=content)


@pytest.mark.django_db
def test_list_school_news_usecase():
    """
    학교에 해당하는 뉴스를 조회할 수 있는지 테스트. 반환되는 뉴스 id는 내림차순이어야 한다.
    """
    # given
    user = UserFactory()
    school = SchoolFactory(owner_id=user.id)
    news1 = SchoolNewsFactory(school_id=school.id)
    news2 = SchoolNewsFactory(school_id=school.id)

    # when
    news = list_school_news_usecase(school_repo=DjangoOrmSchoolsRepo(), school_id=school.id)

    # then
    assert len(news) == 2
    assert news[0] == news2.to_entity()
    assert news[1] == news1.to_entity()


@pytest.mark.django_db
def test_list_school_news_usecase_with_empty_news():
    """
    뉴스가 없는 학교에 대해 뉴스를 조회할 수 있는지 테스트
    """
    # given
    user = UserFactory()
    school = SchoolFactory(owner_id=user.id)

    # when
    news = list_school_news_usecase(school_repo=DjangoOrmSchoolsRepo(), school_id=school.id)

    # then
    assert len(news) == 0


@pytest.mark.django_db
def test_update_school_news_usecase():
    """
    학교 소식을 수정할 수 있는지 테스트
    """
    # given
    user = UserFactory()
    school = SchoolFactory(owner_id=user.id)
    news = SchoolNewsFactory(school_id=school.id)
    content = "new content"

    # when
    update_school_news_usecase(school_repo=DjangoOrmSchoolsRepo(), owner_id=user.id, news_id=news.id, content=content)

    # then
    news = SchoolNews.objects.get(id=news.id)
    assert news.content == content


@pytest.mark.django_db
def test_update_school_news_usecase_with_not_owned_news():
    """
    소유하지 않은 소식을 수정할 수 없는지 테스트
    """
    # given
    owner = UserFactory()
    not_owner = UserFactory()
    school = SchoolFactory(owner_id=owner.id)
    news = SchoolNewsFactory(school_id=school.id)
    content = "new content"

    # when
    with pytest.raises(Unauthorized):
        repo = DjangoOrmSchoolsRepo()
        update_school_news_usecase(school_repo=repo, owner_id=not_owner.id, news_id=news.id, content=content)


@pytest.mark.django_db
def test_delete_school_news_usecase():
    """
    학교 소식을 삭제할 수 있는지 테스트
    """
    # given
    user = UserFactory()
    school = SchoolFactory(owner_id=user.id)
    news = SchoolNewsFactory(school_id=school.id)

    # when
    repo = DjangoOrmSchoolsRepo()
    delete_school_news_usecase(school_repo=repo, owner_id=user.id, news_id=news.id)

    # then
    assert not SchoolNews.objects.filter(id=news.id).exists()


@pytest.mark.django_db
def test_delete_school_news_usecase_with_not_owned_news():
    """
    소유하지 않은 소식을 삭제할 수 없는지 테스트
    """
    # given
    owner = UserFactory()
    not_owner = UserFactory()
    school = SchoolFactory(owner_id=owner.id)
    news = SchoolNewsFactory(school_id=school.id)

    # when
    with pytest.raises(Unauthorized):
        repo = DjangoOrmSchoolsRepo()
        delete_school_news_usecase(school_repo=repo, owner_id=not_owner.id, news_id=news.id)
