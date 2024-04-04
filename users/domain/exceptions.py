from common.exceptions import ClientException


class UserCreateFailed(ClientException):
    msg = "User create failed"
    code = 1003


class UserNotFound(ClientException):
    msg = "User not found"
    code = 1004
