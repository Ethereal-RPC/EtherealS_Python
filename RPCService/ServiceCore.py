from Model.RPCException import RPCException, ErrorCode
from Model.RPCTypeConfig import RPCTypeConfig
from RPCNet import NetCore
from RPCNet.Net import Net
from RPCService.Service import Service
from RPCService.ServiceConfig import ServiceConfig
from Utils.Event import Event

def Get(**kwargs) -> Service:
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("service_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        return None
    return net.services.get(service_name, None)


def Register(**kwargs):
    instance = kwargs.get("instance")
    service_name = kwargs.get("service_name")
    net = kwargs.get("net")
    if kwargs.get("config") is None:
        config: ServiceConfig = ServiceConfig(kwargs.get("type_config"))
    else:
        config: ServiceConfig = kwargs.get("config")
    if net.services.get(service_name, None) is None:
        service = Service()
        service.register(net.name, service_name, instance, config)
        net.services[service_name] = service
        service.log_event.Register(net.OnLog)
        service.exception_event.Register(net.OnException)
        return service
    else:
        raise RPCException(ErrorCode.Core, "{0}-{1}Service已经注册".format(net.name, service_name))


def UnRegister(**kwargs):
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("service_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        raise RPCException(ErrorCode.Runtime, "{0}Net未注册！".format(net_name))
    if net.services.get(service_name, None) is not None:
        del net.services[service_name]
        return True
    return False
