from common.exceptions import ClientException


class SubscriptionNotFound(ClientException):
    code = 1005
    msg = "Subscription not found"


class SubscriptionCreateFailed(ClientException):
    code = 1006
    msg = "Subscription create failed"
