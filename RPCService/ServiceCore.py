from Model.RPCException import RPCException, ErrorCode
from Model.RPCTypeConfig import RPCTypeConfig
from RPCNet import NetCore
from RPCService.Service import Service
from RPCService.ServiceConfig import ServiceConfig


def GetByKey(key: (str, str, str)) -> Service:
    net = NetCore.Get((key[0], key[1]))
    if net is None:
        raise RPCException(ErrorCode.RuntimeError, "{0}-{1}Net未注册！".format(key[0], key[1]))
    return net.services.get(key[2], None)


def GetByStr(ip, port, service_name) -> Service:
    net = NetCore.Get((ip, port))
    if net is None:
        raise RPCException(ErrorCode.RuntimeError, "{0}-{1}Net未注册！".format(ip, port))
    return net.services.get(service_name)


def RegisterByType(instance, ip, port, service_name, rpc_type: RPCTypeConfig):
    return RegisterByConfig(instance, ip, port, service_name, ServiceConfig(rpc_type))


def RegisterByConfig(instance, ip, port, service_name, config):
    net = NetCore.Get((ip, port))
    if net is None:
        raise RPCException(ErrorCode.RuntimeError, "{0}-{1}Net未注册！".format(ip, port))
    if net.services.get(service_name, None) is None:
        service = Service()
        service.register((ip, port), service_name, instance, config)
        net.services[service_name] = service
        return service
    else:
        raise RPCException(ErrorCode.RegisterError, "{0}-{1}-{2}Service已经注册"
                           .format(ip, port, service_name))


def UnRegister(key: (str, str, str)):
    net = NetCore.Get((key[0], key[1]))
    if net is None:
        raise RPCException(ErrorCode.RuntimeError, "{0}-{1}Net未注册！".format(key[0], key[1]))
    if net.services.get(key, None) is not None:
        del net.services[key]
        return True
    return False
