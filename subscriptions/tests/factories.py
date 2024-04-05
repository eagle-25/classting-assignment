import factory


class SubscriptionsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "subscriptions.Subscriptions"

    publisher = factory.SubFactory("users.tests.factories.UsersFactory")
    subscriber = factory.SubFactory("users.tests.factories.UsersFactory")
    is_deleted = False
    deleted_at = None
