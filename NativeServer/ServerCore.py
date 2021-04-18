from Model.RPCException import RPCException
from NativeServer import SocketListener, ServerConfig

__socket_servers = dict()


def RegisterByMethod(ip, port, create_method) -> SocketListener:
    return RegisterByConfig(ip, port, ServerConfig.ServerConfig(create_method))


def RegisterByConfig(ip, port, config) -> SocketListener:
    key = (ip, port)
    if __socket_servers.get(key, None) is None:
        __socket_servers[key] = SocketListener.SocketListener((ip, port), config)
        return __socket_servers[key]
    else:
        raise RPCException(RPCException.ErrorCode.RegisterError, "{0}-{1}Server已经注册".format(ip, port))


def GetByKey(key: (str, str)):
    return __socket_servers.get(key, None)


def GetByStr(ip, port):
    return __socket_servers.get((ip, port), None)


def UnRegister(ip, port):
    if __socket_servers.get((ip, port), None) is not None:
        del __socket_servers[(ip, port)]
        return True
    return False
