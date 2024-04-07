from django.urls import path

from schools.views import SchoolNewsView, SchoolView

urlpatterns = [
    path("<int:school_id>/news", SchoolNewsView.as_view(), name="create_and_read_school_news_view"),  # GET, POST
    path("news/<int:news_id>", SchoolNewsView.as_view(), name="update_and_delete_school_news_view"),  # PATCH, DELETE
    path("", SchoolView.as_view(), name="get_or_create_school_view"),  # GET, POST
]
