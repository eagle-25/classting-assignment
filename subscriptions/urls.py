from django.urls import path

from subscriptions.views import SubscriptionsView, list_school_news

urlpatterns = [
    path("news", list_school_news, name="list_school_news"),  # GET
    path("<int:school_id>", SubscriptionsView.as_view(), name="delete_subscription_view"),  # DELETE
    path("", SubscriptionsView.as_view(), name="create_or_get_subscriptions_view"),  # POST, GET
]
