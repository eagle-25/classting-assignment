import pytest

from users.adapters.repos.django_user_repo import DjangoOrmUserRepo
from users.domain.entities import UserEntity
from users.domain.exceptions import UserCreateFailed, UserNotFound
from users.domain.values import UserType
from users.models import Users
from users.tests.factories import UsersFactory


@pytest.mark.django_db
def test_get_django_user_repo():
    """
    사용자를 조회할 수 있는지 테스트한다.
    """
    # given
    user = UsersFactory(user_type=UserType.PUBLISHER)

    # when
    repo = DjangoOrmUserRepo()
    res = repo.get(user_id=user.id)

    # then
    assert res.id == user.id


@pytest.mark.django_db
def test_get_django_user_repo_not_found():
    """
    사용자가 존재하지 않을 때 UserNotFound 예외가 발생하는지 테스트한다.
    """
    # given
    user_id = 1

    # when, then
    with pytest.raises(UserNotFound):
        DjangoOrmUserRepo().get(user_id=user_id)


@pytest.mark.django_db
def test_django_user_repo_get_by_email_and_password():
    """
    email과 password로 사용자를 조회할 수 있는지 테스트한다.
    """
    # given
    user_id = 1
    email = "abc@example.com"
    password = "password"
    UsersFactory(id=user_id, email=email, password=password, user_type=UserType.PUBLISHER)

    # when
    res = DjangoOrmUserRepo().get_by_email_and_password(email=email, password=password)

    # then
    assert res.id == user_id


@pytest.mark.django_db
def test_django_user_repo_get_by_email_and_password_not_found():
    """
    사용자가 존재하지 않을 때 UserNotFound 예외가 발생하는지 테스트한다.
    """
    # given
    UsersFactory(user_type=UserType.PUBLISHER)

    # when, then
    with pytest.raises(UserNotFound):
        DjangoOrmUserRepo().get_by_email_and_password(email="_", password="_")


@pytest.mark.django_db
def test_django_user_repo_create():
    """
    사용자를 생성할 수 있는지 테스트한다.
    """
    # given
    entity = UserEntity(email="abc@example.com", password="password", user_type=UserType.PUBLISHER)

    # when
    DjangoOrmUserRepo().create(entity=entity)

    # then
    assert Users.objects.filter(email=entity.email).exists()


@pytest.mark.django_db
def test_django_user_repo_create_failed():
    """
    이미 사용중인 email로 user를 생성하려고 하는 경우 UserCreateFailed 예외가 발생하는지 테스트한다.
    """
    # given
    email = "abc@example.com"
    UsersFactory(email=email)

    # when, then
    entity = UserEntity(email=email, password="_", user_type=UserType.PUBLISHER)
    with pytest.raises(UserCreateFailed):
        DjangoOrmUserRepo().create(entity=entity)
