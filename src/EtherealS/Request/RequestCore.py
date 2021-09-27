from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Net import NetCore
from EtherealS.Net.Abstract.Net import Net, NetType
from EtherealS.Request.Abstract.Request import Request
from EtherealS.Request.Abstract.RequestConfig import RequestConfig
from EtherealS.Request.WebSocket.WebSocketRequest import WebSocketRequest
from EtherealS.Request.WebSocket.WebSocketRequestConfig import WebSocketRequestConfig


def Get(**kwargs):
    net_name = kwargs.get("net_name")
    request_name = kwargs.get("service_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        return None
    request = net.requests.get(request_name)
    if request is not None:
        return request.instance
    return None


def GetRequest(**kwargs) -> Request:
    net_name = kwargs.get("net_name")
    request_name = kwargs.get("service_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        return None
    return net.requests.get(request_name)


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
        request.register(instance, net.net_name, service_name, config)
        net.requests[service_name] = request
        request.log_event.Register(net.OnLog)
        request.exception_event.Register(net.OnException)
    else:
        raise TrackException(ExceptionCode.Core, "{0}-{1}已注册，无法重复注册！".format(net.net_name, service_name))
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
