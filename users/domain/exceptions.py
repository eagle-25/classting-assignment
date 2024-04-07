from common.exceptions import ClientException


class UserCreateFailed(ClientException):
    msg = "User create failed"
    code = 2001


class UserNotFound(ClientException):
    msg = "User not found"
    code = 2002
