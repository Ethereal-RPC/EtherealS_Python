from Model.RPCException import RPCException
from RPCNet.NetConfig import NetConfig

__cofigs = dict()


def Get(key: (str, str)) -> NetConfig:
    return __cofigs.get(key, None)


def RegisterByInstanceMethod(ip: str, port: str, instance_method: staticmethod):
    return RegisterByConfig(ip, port, NetConfig(instance_method))


def RegisterByConfig(ip: str, port: str, config: NetConfig):
    key = (ip, port)
    if __cofigs.get(key, None) is None:
        __cofigs[key] = config
    else:
        raise RPCException(RPCException.ErrorCode.RegisterError, "{0}已注册，无法重复注册！".format(key))
    return __cofigs[key]

