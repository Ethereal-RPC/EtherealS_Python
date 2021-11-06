from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Net import NetCore
from EtherealS.Request.Abstract.Request import Request


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
    request = net.requests.get(service_name)
    if request is not None:
        return request
    return None


def Register(request: Request, net):
    if net.requests.get(request.name, None) is None:
        from EtherealS.Request import Abstract
        Abstract.Request.register(net)
        request.net = net
        net.requests[request.name] = request
        request.log_event.Register(net.OnLog)
        request.exception_event.Register(net.OnException)
    else:
        raise TrackException(ExceptionCode.Core, "{0}-{1}已注册，无法重复注册！".format(net.name, request.name))
    return request


def UnRegister(request: Request):
    if request.net.requests.get(request.name, None) is not None:
        del request.net.requests[request.name]
    request.net = None
    return True
