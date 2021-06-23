from Model.RPCException import RPCException, ErrorCode
from NativeServer import SocketListener, ServerConfig
from RPCNet import NetCore
from RPCNet.Net import Net


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


def Register(**kwargs) -> SocketListener:
    net: Net = kwargs.get("net")
    ip = kwargs.get("ip")
    port = kwargs.get("port")
    create_method = kwargs.get("create_method")
    if create_method is not None:
        config = ServerConfig.ServerConfig(create_method)
    else:
        config = kwargs.get("config")
    if net.server is None:
        net.server = SocketListener.SocketListener(net, (ip, port), config)
        return net.server
    else:
        raise RPCException(ErrorCode.Core, "{0} Net 已经拥有Server".format(net.name))


def UnRegister(**kwargs):
    net_name = kwargs.get("net_name")
    if net_name is not None:
        net = NetCore.Get(net_name)
    else:
        net = kwargs.get("net")
    if net.server is not None:
        net.server.doStop()
        net.serverRequestSend = None
        net.clientResponseSend = None
        net.server = None
        return True
    return False
