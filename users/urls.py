from django.urls import path

from users.views import create_user_view, sign_in_view

urlpatterns = [
    path("sign-in", sign_in_view, name="sign_in_view"),
    path("", create_user_view, name="create_user_view"),
]
