from django.urls import path

from users.views import create_user_view

urlpatterns = [
    path("sign_in/", create_user_view, name="sign_in_view"),  # GET
    path("", create_user_view, name="create_user_view"),  # POST
]
