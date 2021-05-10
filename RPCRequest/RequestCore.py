from Model.RPCException import RPCException, ErrorCode
from Model.RPCTypeConfig import RPCTypeConfig
from RPCNet import NetCore
from RPCRequest.Request import Request
from RPCRequest.RequestConfig import RequestConfig


def GetByStr(ip: str, port: str, request_name: str) -> Request:
    net = NetCore.Get((ip, port))
    if net is None:
        raise RPCException(ErrorCode.RuntimeError, "{0}-{1}Net未注册！".format(ip, port))
    return net.requests.get(request_name, None)


def GetByKey(key: (str, str, str)) -> Request:
    net = NetCore.Get((key[0], key[1]))
    if net is None:
        raise RPCException(ErrorCode.RuntimeError, "{0}-{1}Net未注册！".format(key[0], key[1]))
    return net.requests.get(key[2], None)


def RegisterByType(instance, ip: str, port: str, service: str, types: RPCTypeConfig):
    return RegisterByConfig(instance, ip, port, service, RequestConfig(types))


def RegisterByConfig(instance, ip: str, port: str, service_name: str, config: RequestConfig):
    net = NetCore.Get((ip, port))
    if net is None:
        raise RPCException(ErrorCode.RuntimeError, "{0}-{1}Net未注册！".format(ip, port))
    if net.requests.get(service_name, None) is None:
        request = Request(config)
        request.register(instance, (ip, port), service_name, config)
        net.requests[service_name] = request
    else:
        raise RPCException(ErrorCode.RegisterError, "{0}已注册，无法重复注册！".format((ip,port,service_name)))
    return instance


def UnRegister(ip: str, port: str, service_name: str):
    net = NetCore.Get((ip, port))
    if net is None:
        raise RPCException(ErrorCode.RuntimeError, "{0}-{1}Net未注册！".format(ip, port))
    if net.requests.get(service_name, None) is not None:
        del net.requests[service_name]
        return True
    return False
