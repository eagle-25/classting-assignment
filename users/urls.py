from django.urls import re_path

from users import views

urlpatterns = [
    re_path("sign-in", views.sign_in_view, name="sign_in_view"),
    re_path("sign-up", views.sign_up_view, name="sign_up_view"),
]
