from django.urls import re_path

from subscriptions import views

urlpatterns = [
    re_path(
        r"(?P<publisher_id>\d+)/",
        views.SubscriptionsView.as_view(),
        name="delete_subscription_view",
    ),  # DELETE
    re_path("", views.SubscriptionsView.as_view(), name="create_or_get_subscription_view"),  # GET, POST
]
