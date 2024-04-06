class ClasstingException(Exception):
    def __init__(self, detail: str | None = None):
        self.detail = detail

    status = 500
    code = 1000
    msg = "Unknown error"


class ServiceException(ClasstingException):
    status = 500
    code = 1000
    msg = "Service Exception"


class ClientException(ClasstingException):
    status = 400
    code = 1000
    msg = "Client error"


class InvalidParameter(ClientException):
    code = 1001
    msg = "Invalid parameter"


class ValueNotFound(ClientException):
    code = 1002
    status = 404
    msg = "Value not found"


class ValidationFailed(ClientException):
    code = 1003
    msg = "Validation failed"
