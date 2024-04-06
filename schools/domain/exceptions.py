from common.exceptions import ClientException


class SchoolCreateFailed(ClientException):
    code = 3001
    status = 400
    msg = "School create failed"


class SchoolNotFound(ClientException):
    code = 3002
    status = 404
    msg = "School not found"
