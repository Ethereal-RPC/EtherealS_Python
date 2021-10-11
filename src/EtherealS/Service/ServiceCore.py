from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Net import NetCore
from EtherealS.Service.Abstract.Service import Service


def Get(**kwargs):
    from EtherealS.Net.Abstract.Net import Net
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("service_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        return None
    return net.services.get(service_name, None)


def Register(service: Service, net):
    if net.services.get(service.name, None) is None:
        from EtherealS.Service import Abstract
        Abstract.Service.register(service)
        service.net_name = net.name
        net.services[service.name] = service
        service.log_event.Register(net.OnLog)
        service.exception_event.Register(net.OnException)
        return service
    else:
        raise TrackException(ExceptionCode.Core, "{0}-{1}Service已经注册".format(net.name, service.name))


def UnRegister(**kwargs):
    from EtherealS.Net.Abstract.Net import Net
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
