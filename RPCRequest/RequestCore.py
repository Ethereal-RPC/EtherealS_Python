from Model.RPCException import RPCException, ExceptionCode
from RPCNet import NetCore
from RPCNet.Net import Net
from RPCRequest.Request import Request
from RPCRequest.RequestConfig import RequestConfig


def Get(**kwargs) -> Request:
    net_name = kwargs.get("net_name")
    request_name = kwargs.get("name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        return None
    return net.services.get(request_name)


def Register(**kwargs):
    instance = kwargs.get("instance")
    service_name = kwargs.get("name")
    net: Net = kwargs.get("net")
    if kwargs.get("config") is None:
        config: RequestConfig = RequestConfig(kwargs.get("type_config"))
    else:
        config: RequestConfig = kwargs.get("config")
    if net.requests.get(service_name, None) is None:
        request = Request(config)
        request.register(instance, net.name, service_name, config)
        net.requests[service_name] = request
        request.log_event.Register(net.OnLog)
        request.exception_event.Register(net.OnException)
    else:
        raise RPCException(ExceptionCode.Core, "{0}-{1}已注册，无法重复注册！".format(net.name, service_name))
    return instance


def UnRegister(**kwargs):
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is not None:
        if net.requests.get(service_name, None) is not None:
            del net.requests[service_name]
    return True
