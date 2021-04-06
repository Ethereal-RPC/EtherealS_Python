from enum import Enum


class ErrorCode(Enum):
    Intercepted = 1
    NotFoundService = 2
    NotFoundRequest = 3
    RegisterError = 4
    NotFoundNetConfig = 5


class RPCException(Exception):
    ErrorCode = ErrorCode.RegisterError

    def __init__(self, code, msg):
        Exception.__init__(self, code, msg)
