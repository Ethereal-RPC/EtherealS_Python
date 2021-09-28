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
    service = net.services.get(service_name, None)
    if service is not None:
        return service


def Register(instance, net, service_name, types=None, config=None):
    if config is None and types is None:
        raise TrackException(ExceptionCode.Core, "types和config必须提供一个")
    if config is None:
        if net.type == NetType.WebSocket:
            config = WebSocketServiceConfig(types)
        else:
            raise TrackException(ExceptionCode.Core, "未有针对{0}的Service-Register处理".format(net.type))

    if net.services.get(service_name, None) is None:
        from EtherealS.Service import Abstract
        Abstract.Service.register(instance, net.net_name, service_name, config)
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
