from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Net import NetCore
from EtherealS.Service.Abstract.Service import Service


def Get(service_name,net_name=None,net=None) -> Service:
    from EtherealS.Net.Abstract.Net import Net
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    if net is not None:
        return net.services.get(service_name, None)
    return None


def Register(service: Service, net):
    if not service.isRegister:
        from EtherealS.Service import Abstract
        service.isRegister = True
        service.Initialize()
        Abstract.Service.register(service)
        service.net = net
        net.services[service.name] = service
        service.log_event.Register(net.OnLog )
        service.exception_event.Register(net.OnException)
        service.Register()
        return service
    else:
        raise TrackException(ExceptionCode.Core, "{0}-{1}Service已经注册".format(net.name, service.name))


def UnRegister(service: Service) -> Service:
    if service.isRegister:
        service.UnRegister()
        if service.net is not None:
            if service.net.services.get(service.name, None) is not None:
                del service.net.services[service.name]
            service.net = None
        service.UnInitialize()
        service.isRegister = False
        return service
    else:
        raise TrackException(ExceptionCode.Core, "Service:{0}已经UnRegister".format(service.name))
