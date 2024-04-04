class ClasstingException(Exception):
    def __init__(self, detail: str | None = None):
        self.detail = detail

    status = 500
    code = 1000
    msg = "Unknown Error"


class ServerException(ClasstingException):
    status = 500
    code = 1000
    msg = "Server Error"


class ClientException(ClasstingException):
    status = 400
    code = 1000
    msg = "Client Error"


class InvalidParameter(ClientException):
    code = 1001
    msg = "Invalid Parameter"


class ValueNotFound(ClientException):
    code = 1002
    msg = "Value Not Found"
