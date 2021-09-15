import RPCRequest.RequestCore
import RPCService.ServiceCore
from RPCNet.Net import Net
from RPCNet.NetConfig import NetConfig

nets = dict()


def Get(name) -> Net:
    return nets.get(name)


def Register(**kwargs) -> Net:
    name = kwargs.get("name")
    config: NetConfig = kwargs.get("config")
    if config is None:
        config = NetConfig()
    if nets.get(name, None) is None:
        net = Net()
        net.name = name
        net.config = config
        nets[name] = net
    else:
        return None
    return nets[name]


def UnRegister(**kwargs):
    name = kwargs.get("name")
    if name is not None:
        net = Get(name)
        if net is not None:
            for request in net.requests:
                RPCRequest.RequestCore.UnRegister(net_name=net, service_name=request.name)
            for service in net.services:
                RPCService.ServiceCore.UnRegister(net_name=net, service_name=service.name)
            del nets[name]
    return True
