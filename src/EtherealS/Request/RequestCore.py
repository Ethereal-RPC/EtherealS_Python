from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Net import NetCore
from EtherealS.Net.Abstract.Net import Net, NetType
from EtherealS.Request.Abstract.Request import Request
from EtherealS.Request.Abstract.RequestConfig import RequestConfig
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
        return request
    return None


def Register(instance, net, service_name, types, config=None):
    if net.requests.get(service_name, None) is None:
        from EtherealS.Request import Abstract
        Abstract.Request.register(instance, net.net_name, service_name, types, config)
        net.requests[service_name] = instance
        instance.log_event.Register(net.OnLog)
        instance.exception_event.Register(net.OnException)
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
