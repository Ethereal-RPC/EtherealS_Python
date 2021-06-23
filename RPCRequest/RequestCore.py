from Model.RPCException import RPCException, ErrorCode
from Model.RPCTypeConfig import RPCTypeConfig
from RPCNet import NetCore
from RPCNet.Net import Net
from RPCRequest.Request import Request
from RPCRequest.RequestConfig import RequestConfig


def Get(**kwargs) -> Request:
    net_name = kwargs.get("net_name")
    request_name = kwargs.get("request_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        raise RPCException(ErrorCode.Runtime, "{0}Net未注册！".format(net_name))
    return net.services.get(request_name)


def RegisterByConfig(**kwargs):
    instance = kwargs.get("instance")
    service_name = kwargs.get("request_name")
    net = kwargs.get("net")
    if kwargs.get("type_config") is not None:
        config: RequestConfig = RequestConfig(kwargs.get("type_config"))
    else:
        config: RequestConfig = kwargs.get("config")
    if net.requests.get(service_name, None) is None:
        request = Request(config)
        request.register(instance, net.name, service_name, config)
        net.requests[service_name] = request
    else:
        raise RPCException(ErrorCode.Core, "{0}-{1}已注册，无法重复注册！".format(net.name, service_name))
    return instance


def UnRegister(**kwargs):
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("service_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        raise RPCException(ErrorCode.Runtime, "{0}Net未注册！".format(net_name))
    if net.requests.get(service_name, None) is not None:
        del net.requests[service_name]
        return True
    return False
