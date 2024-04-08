from common.exceptions import ClientException


class UserAlreadyExists(ClientException):
    msg = "User already exists"
    code = 2001
    status = 409


class UserNotFound(ClientException):
    msg = "User not found"
    code = 2002
