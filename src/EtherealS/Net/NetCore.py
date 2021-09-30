import EtherealS.Request.RequestCore
import EtherealS.Service.ServiceCore
from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Net.Abstract.Net import Net, NetType
from EtherealS.Net.Abstract.NetConfig import NetConfig
from EtherealS.Net.WebSocket.WebSocketNet import WebSocketNet
from EtherealS.Net.WebSocket.WebSocketNetConfig import WebSocketNetConfig

nets = dict()


def Get(name) -> Net:
    return nets.get(name)


def Register(net: Net) -> Net:
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
