from django.urls import re_path

from users.views import UsersView

urlpatterns = [
    re_path("", UsersView.as_view(), name="users_view"),
]
