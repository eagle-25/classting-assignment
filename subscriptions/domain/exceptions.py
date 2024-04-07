from common.exceptions import ClientException


class SubscriptionCancelFailed(ClientException):
    status = 400
    code = 4001
    msg = 'Subscription cancel failed'


class SubscriptionCreateFailed(ClientException):
    status = 400
    code = 4002
    msg = 'Subscription create failed'
