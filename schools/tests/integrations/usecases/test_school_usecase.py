import pytest

from common.exceptions import Unauthorized
from schools.adapters.repos.school_repo import DjangoOrmSchoolsRepo
from schools.tests.factories import SchoolFactory, SchoolNewsFactory
from schools.usecases.school_usecase import (
    create_school_news_usecase,
    delete_school_news_usecase,
    update_school_news_usecase,
)
from users.tests.factories import UserFactory


@pytest.mark.django_db
def create_school_news_usecase_with_not_owned_school():
    """
    소유하지 않은 학교에 소식을 생성할 수 없는지 테스트
    """
    # given
    owner = UserFactory()
    school = SchoolFactory(owner_id=owner.id)

    # when
    not_owner = UserFactory()

    with pytest.raises(Unauthorized):
        repo = DjangoOrmSchoolsRepo()
        create_school_news_usecase(school_repo=repo, owner_id=not_owner.id, school_id=school.id, content="")


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
