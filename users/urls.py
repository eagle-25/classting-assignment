from django.urls import path

from users.views import sign_in_view, sign_up_view

urlpatterns = [
    path("sign-in", sign_in_view, name="sign_in_view"),
    path("sign-up", sign_up_view, name="sign_up_view"),
]
