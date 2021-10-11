import EtherealS.Request.RequestCore
import EtherealS.Service.ServiceCore

nets = dict()


def Get(name):
    return nets.get(name)


def Register(net):
    if nets.get(net.name, None) is None:
        nets[net.name] = net
    else:
        return None
    return net


def UnRegister(**kwargs):
    name = kwargs.get("net_name")
    if name is not None:
        net = Get(name)
        if net is not None:
            for request in net.requests:
                EtherealS.Request.RequestCore.UnRegister(net_name=net, service_name=request.name)
            for service in net.services:
                EtherealS.Service.ServiceCore.UnRegister(net_name=net, service_name=service.name)
            net.server.Close()
            net.server = None
            del nets[name]
    return True
