from django.urls import path

from users.adapter.income.web.sign_in_view import SignInView
from users.adapter.income.web.sign_up_view import SignUpView
from users.adapter.outcome.persistence.user_persistence_adapter import (
    UserPersistenceAdapter,
)
from users.adapter.outcome.persistence.user_repo import DjangoOrmUserRepo
from users.app.usecase.sign_in_usecase import SignInUseCase
from users.app.usecase.sign_up_usecase import SignUpUsecase

_user_repo = DjangoOrmUserRepo()
_user_persistence_adapter = UserPersistenceAdapter(user_repo=_user_repo)
_sign_in_usecase = SignInUseCase(get_user_port=_user_persistence_adapter)
_sign_up_usecase = SignUpUsecase(create_user_port=_user_persistence_adapter)

urlpatterns = [
    path("sign-in", SignInView(usecase=_sign_in_usecase).handle, name="sign_in_view"),
    path("sign-up", SignUpView(usecase=_sign_up_usecase).handle, name="sign_up_view"),
]
