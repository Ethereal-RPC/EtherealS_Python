from Model.RPCException import RPCException
from Model.RPCTypeConfig import RPCTypeConfig
from RPCService.Service import Service
from RPCService.ServiceConfig import ServiceConfig

__service = dict()


def GetByKey(key) -> Service:
    return __service.get(key, None)


def GetByStr(hostname, port, service_name) -> Service:
    return __service.get((hostname, port, service_name), None)


def RegisterByType(instance, ip, port, service_name, rpc_type: RPCTypeConfig):
    return RegisterByConfig(instance, ip, port, service_name, ServiceConfig(rpc_type))


def RegisterByConfig(instance, ip, port, service_name, config):
    key = (ip, port, service_name)
    if __service.get(key, None) is None:
        service = Service()
        service.register(key, service_name, instance, config)
        __service[key] = service
        return service
    else:
        raise RPCException(RPCException.ErrorCode.RegisterError, "{0}-{1}-{2}Service已经注册"
                           .format(ip, port, service_name))


def UnRegister(key: (str, str, str)):
    if __service.get(key, None) is not None:
        del __service[key]
        return True
    return False
