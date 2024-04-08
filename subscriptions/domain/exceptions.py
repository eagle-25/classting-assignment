from common.exceptions import ClientException


class AlreadySubscribed(ClientException):
    status = 409
    code = 4001
    msg = 'Already subscribed'


class CannotSubscribeToOwnSchool(ClientException):
    status = 400
    code = 4002
    msg = 'Cannot subscribe to own school'


class SubscriptionNotFound(ClientException):
    status = 400
    code = 4003
    msg = 'Subscription not found'
