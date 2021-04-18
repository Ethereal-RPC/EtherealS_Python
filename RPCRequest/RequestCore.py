from Model.RPCException import RPCException
from Model.RPCType import RPCType
from RPCRequest.Request import Request
from RPCRequest.RequestConfig import RequestConfig

__requests = dict()


def GetByStr(ip: str, port: str, request_name: str) -> Request:
    return __requests.get((ip, port, request_name), None)


def GetByKey(key: (str, str, str)) -> Request:
    return __requests.get(key, None)


def RegisterByType(instance, ip: str, port: str, service: str, types: RPCType):
    return RegisterByConfig(instance, ip, port, service, RequestConfig(types))


def RegisterByConfig(instance, ip: str, port: str, service: str, config: RequestConfig):
    key = (ip, port, service)
    if __requests.get(key, None) is None:
        request = Request(config)
        request.register(instance, (ip, port),service, config)
        __requests[key] = request
    else:
        raise RPCException(RPCException.ErrorCode.RegisterError, "{0}已注册，无法重复注册！".format(key))
    return instance


def UnRegister(key: (str, str, str)):
    if __requests.get(key, None) is not None:
        del __requests[key]
