import pytest
from pytest_mock import MockFixture

from common.exceptions import Unauthorized
from schools.adapters.repos.school_repo import DjangoOrmSchoolsRepo
from schools.usecases.school_usecase import (
    create_school_news_usecase,
    delete_school_news_usecase,
    update_school_news_usecase,
)


def test_create_school_news_usecase_with_not_owned_school(mocker: MockFixture):
    """
    소유하지 않은 학교에 소식을 생성할 수 없는지 테스트
    """
    # given
    mocker.patch.object(DjangoOrmSchoolsRepo, "is_owned_school", return_value=False)

    # when
    with pytest.raises(Unauthorized):
        repo = DjangoOrmSchoolsRepo()
        create_school_news_usecase(repo, owner_id=1, school_id=1, content="content")


def test_create_school_news_usecase(mocker: MockFixture):
    """
    소유한 학교의 소식을 생성할 때, 소식 생성 로직을 기대한대로 호출하는지 테스트
    """
    # given
    mocker.patch.object(DjangoOrmSchoolsRepo, "is_owned_school", return_value=True)
    create_action = mocker.patch.object(DjangoOrmSchoolsRepo, "create_school_news")

    # when
    repo = DjangoOrmSchoolsRepo()
    create_school_news_usecase(repo, owner_id=1, school_id=1, content="content")

    # then
    create_action.assert_called_once_with(school_id=1, content="content")


def test_update_school_news_usecase_with_not_owned_news(mocker: MockFixture):
    """
    소유하지 않은 소식을 수정할 수 없는지 테스트
    """
    # given
    mocker.patch.object(DjangoOrmSchoolsRepo, "is_owned_news", return_value=False)

    # when
    with pytest.raises(Unauthorized):
        repo = DjangoOrmSchoolsRepo()
        update_school_news_usecase(school_repo=repo, owner_id=1, news_id=2, content="")


def test_update_school_news_usecase(mocker: MockFixture):
    """
    소유한 소식을 수정할 때, 소식 수정 로직을 기대한대로 호출하는지 테스트
    """
    # given
    mocker.patch.object(DjangoOrmSchoolsRepo, "is_owned_news", return_value=True)
    update_action = mocker.patch.object(DjangoOrmSchoolsRepo, "update_school_news")

    # when
    repo = DjangoOrmSchoolsRepo()
    update_school_news_usecase(school_repo=repo, owner_id=1, news_id=2, content="content")

    # then
    update_action.assert_called_once_with(news_id=2, content="content")


def test_delete_school_news_usecase_with_not_owned_news(mocker: MockFixture):
    """
    소유하지 않은 소식을 삭제할 수 없는지 테스트
    """
    # given
    mocker.patch.object(DjangoOrmSchoolsRepo, "is_owned_news", return_value=False)

    # when
    with pytest.raises(Unauthorized):
        repo = DjangoOrmSchoolsRepo()
        delete_school_news_usecase(school_repo=repo, owner_id=1, news_id=2)


def test_delete_school_news_usecase(mocker: MockFixture):
    """
    소유한 소식을 삭제할 때, 소식 삭제 로직을 기대한대로 호출하는지 테스트
    """
    # given
    mocker.patch.object(DjangoOrmSchoolsRepo, "is_owned_news", return_value=True)
    delete_action = mocker.patch.object(DjangoOrmSchoolsRepo, "delete_school_news")

    # when
    repo = DjangoOrmSchoolsRepo()
    delete_school_news_usecase(school_repo=repo, owner_id=1, news_id=2)

    # then
    delete_action.assert_called_once_with(news_id=2)
