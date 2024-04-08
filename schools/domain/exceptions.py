from common.exceptions import ClientException


class SchoolAlreadyExists(ClientException):
    code = 3001
    msg = "School already exists"


class SchoolNotFound(ClientException):
    code = 3002
    msg = "School not found"


class SchoolNewsCreateFailed(ClientException):
    code = 3003
    msg = "School news create failed"


class SchoolNewsNotFound(ClientException):
    code = 3004
    msg = "School news not found"
