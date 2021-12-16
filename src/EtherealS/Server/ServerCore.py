from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Server.Abstract.ServerConfig import ServerConfig
from EtherealS.Server.Abstract.Server import Server
from EtherealS.Net import NetCore
from EtherealS.Net.Abstract.Net import Net, NetType
from EtherealS.Server.WebSocket.WebSocketServer import WebSocketServer
from EtherealS.Server.WebSocket.WebSocketServerConfig import WebSocketServerConfig


def Get(net_name):
    net = NetCore.Get(net_name)
    if net is not None:
        return net.server
    return None


def Register(net: Net, server: Server) -> Server:
    if not server.isRegister:
        server.isRegister = True
        net.server = server
        server.net = net
        server.log_event.Register(net.OnLog)
        server.exception_event.Register(net.OnException)
        return server
    else:
        raise TrackException(ExceptionCode.Core, "{0} Net 已经拥有Server".format(net.name))


def UnRegister(server: Server):
    if server.isRegister:
        if server.net is not None:
            server.net.server = None
            server.net = None
        server.Close()
        server.isRegister = False
        return True
    else:
        raise TrackException(ExceptionCode.Core, "{0}已经UnRegister".format(server.name))