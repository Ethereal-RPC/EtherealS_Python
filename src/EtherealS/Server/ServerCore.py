from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Server.Abstract.ServerConfig import ServerConfig
from EtherealS.Server.Abstract.Server import Server
from EtherealS.Net import NetCore
from EtherealS.Net.Abstract.Net import Net, NetType
from EtherealS.Server.WebSocket.WebSocketServer import WebSocketServer
from EtherealS.Server.WebSocket.WebSocketServerConfig import WebSocketServerConfig


def Get(**kwargs):
    net_name = kwargs.get("net_name")
    if net_name is not None:
        net = NetCore.Get(net_name)
    else:
        net = kwargs.get("net")
    if net is not None:
        return net.server
    else:
        return None


def Register(**kwargs) -> Server:
    net: Net = kwargs.get("net")
    prefixes = kwargs.get("prefixes")
    create_method = kwargs.get("create_method")
    if create_method is not None:
        if net.type == NetType.WebSocket:
            config = WebSocketServerConfig(create_method)
        else:
            raise TrackException(ExceptionCode.Core, "未有针对{0}的Server-Register处理".format(net.type))
    else:
        config = kwargs.get("config")
    if net.server is None:
        if net.type == NetType.WebSocket:
            net.server = WebSocketServer(net_name=net.net_name, prefixes=prefixes, config=config)
        else:
            raise TrackException(ExceptionCode.Core, "未有针对{0}的Server-Register处理".format(net.type))

        def onLog(**kwargs):
            net.OnLog(**kwargs)

        def onException(**kwargs):
            net.OnException(**kwargs)

        net.server.log_event.Register(onLog)
        net.server.exception_event.Register(onException)
        return net.server
    else:
        raise TrackException(ExceptionCode.Core, "{0} Net 已经拥有Server".format(net.net_name))


def UnRegister(**kwargs):
    net_name = kwargs.get("net_name")
    if net_name is not None:
        net = NetCore.Get(net_name)
    else:
        net = kwargs.get("net")
    if net.server is not None:
        net.server.Close()
        net.server = None
    return True
