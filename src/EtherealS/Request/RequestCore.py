from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Net import NetCore
from EtherealS.Request.Abstract.Request import Request
from EtherealS.Service import ServiceCore
from EtherealS.Service.Abstract.Service import Service


def Get(net=None, net_name=None, service: Service=None, service_name=None, request_name=None):
    from EtherealS.Net.Abstract.Net import Net
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    if service_name is not None:
        service = ServiceCore.Get(net=net, service_name=service_name)
    if service is not None:
        return service.requests.get(request_name)
    return None


def Register(request: Request, service):
    if not request.isRegister:
        request.isRegister = True
        request.Initialize()
        from EtherealS.Request import Abstract
        Abstract.Request.register(service)
        request.service = service
        service.requests[request.name] = request
        request.log_event.Register(service.OnLog)
        request.exception_event.Register(service.OnException)
        request.Register()
    else:
        raise TrackException(ExceptionCode.Core, "{0}-{1}已注册，无法重复注册！".format(service.name, request.name))
    return request


def UnRegister(request: Request):
    if request.isRegister:
        request.UnRegister()
        if request.service is not None:
            if request.service.requests.__contains__(request.name):
                del request.service.requests[request.name]
            request.service = None
        request.isRegister = False
        request.UnInitialize()
    else:
        raise TrackException(ExceptionCode.Core, "{0}已经UnRegister".format(request.name))
