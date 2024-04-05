from django.urls import re_path

from subscriptions import views

urlpatterns = [
    re_path("", views.SubscriptionsView.as_view(), name="create_subscription_view"),
]
