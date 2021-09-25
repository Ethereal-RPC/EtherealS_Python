from Core.Model.TrackException import TrackException, ExceptionCode
from Net import NetCore
from Net.Abstract.Net import Net, NetType
from Request.Abstract.Request import Request
from Request.Abstract.RequestConfig import RequestConfig
from Request.WebSocket.WebSocketRequest import WebSocketRequest
from Request.WebSocket.WebSocketRequestConfig import WebSocketRequestConfig


def Get(**kwargs) -> Request:
    net_name = kwargs.get("net_name")
    request_name = kwargs.get("service_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        return None
    return net.services.get(request_name)


def Register(**kwargs):
    instance = kwargs.get("instance")
    service_name = kwargs.get("service_name")
    net: Net = kwargs.get("net")
    if kwargs.get("config") is None:
        if net.type == NetType.WebSocket:
            config: RequestConfig = WebSocketRequestConfig(kwargs.get("types"))
        else:
            raise TrackException(ExceptionCode.Core, "未有针对{0}的Request-Register处理".format(net.type))
    else:
        config: RequestConfig = kwargs.get("config")
    if net.requests.get(service_name, None) is None:
        if net.type == NetType.WebSocket:
            request = WebSocketRequest(config)
        else:
            raise TrackException(ExceptionCode.Core, "未有针对{0}的Request-Register处理".format(net.type))
        request.register(instance, net.name, service_name, config)
        net.requests[service_name] = request
        request.log_event.Register(net.OnLog)
        request.exception_event.Register(net.OnException)
    else:
        raise TrackException(ExceptionCode.Core, "{0}-{1}已注册，无法重复注册！".format(net.name, service_name))
    return instance


def UnRegister(**kwargs):
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("service_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is not None:
        if net.requests.get(service_name, None) is not None:
            del net.requests[service_name]
    return True
