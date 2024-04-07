from datetime import datetime, timezone

from factory.django import DjangoModelFactory

from subscriptions.models import Subscriptions


class SubscriptionFactory(DjangoModelFactory):
    class Meta:
        model = Subscriptions

    subscribed_at = datetime.now(tz=timezone.utc)
    canceled_at = None
