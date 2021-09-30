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


def Register(net: Net, server: Server) -> Server:
    if net.server is None:
        def onLog(**kwargs):
            net.OnLog(**kwargs)

        def onException(**kwargs):
            net.OnException(**kwargs)

        net.server = server
        server.net_name = net.name
        net.server.log_event.Register(onLog)
        net.server.exception_event.Register(onException)
        return net.server
    else:
        raise TrackException(ExceptionCode.Core, "{0} Net 已经拥有Server".format(net.name))


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
