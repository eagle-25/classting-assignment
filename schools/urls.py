from django.urls import path

from schools.views import SchoolNewsView, SchoolView, list_owned_schools

urlpatterns = [
    path("news", SchoolNewsView.as_view(), name="create_or_read_school_news_view"),  # GET, POST
    path("news/<int:news_id>", SchoolNewsView.as_view(), name="update_or_delete_school_news_view"),  # PATCH, DELETE
    path("owned", list_owned_schools, name="list_owned_schools"),  # GET
    path("", SchoolView.as_view(), name="get_or_create_school_view"),  # GET, POST
]
