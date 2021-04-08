from Model.RPCException import RPCException
from Model.RPCType import RPCType
from RPCRequest.Request import Request
from RPCRequest.RequestConfig import RequestConfig

__requests = dict()


def GetByStr(request_name: str, ip: str, port: str) -> Request:
    return __requests.get((request_name, ip, port), None)


def GetByKey(key: (str, str, str)) -> Request:
    return __requests.get(key, None)


def RegisterByType(service: str, ip: str, port: str, types: RPCType):
    return RegisterByConfig(service, ip, port, RequestConfig(types))


def RegisterByConfig(service: str, ip: str, port: str, config: RequestConfig):
    key = (service, ip, port)
    if __requests.get(key, None) is None:
        __requests[key] = Request(config)
    else:
        raise RPCException(RPCException.ErrorCode.RegisterError, "{0}已注册，无法重复注册！".format(key))
    return __requests[key]


def UnRegister(key: (str, str, str)):
    if __requests.get(key, None) is not None:
        del __requests[key]
