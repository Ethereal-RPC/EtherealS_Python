from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Net import NetCore
from EtherealS.Net.Abstract.Net import Net, NetType
from EtherealS.Service.Abstract.Service import Service
from EtherealS.Service.Abstract.ServiceConfig import ServiceConfig
from EtherealS.Service.WebSocket.WebSocketService import WebSocketService
from EtherealS.Service.WebSocket.WebSocketServiceConfig import WebSocketServiceConfig


def Get(**kwargs):
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("service_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        return None
    return net.services.get(service_name, None)


def Register(instance, net, service_name, types, config=None):
    if net.services.get(service_name, None) is None:
        from EtherealS.Service import Abstract
        Abstract.Service.register(instance, net.net_name, service_name, types, config)
        net.services[service_name] = instance
        instance.log_event.Register(net.OnLog)
        instance.exception_event.Register(net.OnException)
        return instance
    else:
        raise TrackException(ExceptionCode.Core, "{0}-{1}Service已经注册".format(net.service_name, service_name))


def UnRegister(**kwargs):
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("service_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is not None:
        if net.services.get(service_name, None) is not None:
            del net.services[service_name]
    return True
