from Model.RPCException import RPCException, ExceptionCode
from RPCNet import NetCore
from RPCNet.Net import Net
from RPCService.Service import Service
from RPCService.ServiceConfig import ServiceConfig


def Get(**kwargs) -> Service:
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        return None
    return net.services.get(service_name, None)


def Register(instance, net, service_name, types=None, config=None):
    if config is None and types is None:
        raise RPCException(ExceptionCode.Core, "types和config必须提供一个")
    if config is None:
        config = ServiceConfig(types)
    if net.services.get(service_name, None) is None:
        service = Service()
        service.register(net.name, service_name, instance, config)
        net.services[service_name] = service
        service.log_event.Register(net.OnLog)
        service.exception_event.Register(net.OnException)
        return service
    else:
        raise RPCException(ExceptionCode.Core, "{0}-{1}Service已经注册".format(net.name, name))


def UnRegister(**kwargs):
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is not None:
        if net.services.get(service_name, None) is not None:
            del net.services[service_name]
    return True
