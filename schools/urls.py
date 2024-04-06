from django.urls import re_path

from schools.views import SchoolView

urlpatterns = [
    re_path(r"(?P<owner_id>\d+)/", SchoolView.as_view(), name="get_schools_view"),  # GET
    re_path("", SchoolView.as_view(), name="school_view"),  # POST
]
