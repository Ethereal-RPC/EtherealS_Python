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


def Register(**kwargs) -> Net:
    net_name = kwargs.get("net_name")
    config: NetConfig = kwargs.get("config")
    net_type: NetType = kwargs.get("type")
    if net_type == NetType.WebSocket:
        if config is None:
            config = WebSocketNetConfig()
    else:
        raise TrackException(ExceptionCode.Core, "未有针对{0}的Net-Register处理".format(net_type))
    if nets.get(net_name, None) is None:
        if net_type == NetType.WebSocket:
            net = WebSocketNet(net_name=net_name)
        else:
            raise TrackException(ExceptionCode.Core, "未有针对{0}的Net-Register处理".format(net_type))
        net.type = net_type
        net.net_name = net_name
        net.config = config
        nets[net_name] = net
    else:
        return None
    return nets[net_name]


def UnRegister(**kwargs):
    name = kwargs.get("service_name")
    if name is not None:
        net = Get(name)
        if net is not None:
            for request in net.requests:
                EtherealS.Request.RequestCore.UnRegister(net_name=net, service_name=request.service_name)
            for service in net.services:
                EtherealS.Service.ServiceCore.UnRegister(net_name=net, service_name=service.service_name)
            del nets[name]
    return True
