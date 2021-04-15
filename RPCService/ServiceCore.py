import json

from Model.BaseUserToken import BaseUserToken
from Model.ClientRequestModel import ClientRequestModel
from Model.ClientResponseModel import ClientResponseModel
from Model.RPCException import RPCException
from Model.RPCType import RPCType
from RPCNet import NetCore
from RPCNet.NetConfig import NetConfig
from RPCService.Service import Service
from RPCService.ServiceConfig import ServiceConfig

__service = dict()


def GetByKey(key) -> Service:
    return __service.get(key, None)


def GetByStr(service_name, hostname, port) -> Service:
    return __service.get((service_name, hostname, port), None)


def RegisterByType(instance, service_name, ip, port, rpc_type: RPCType):
    return RegisterByConfig(instance, service_name, ip, port, ServiceConfig(rpc_type))


def RegisterByConfig(instance, service_name, ip, port, config):
    key = (service_name, ip, port)
    if __service.get(key, None) is None:
        service = Service()
        service.register(key, instance, config)
        __service[key] = service
        return service
    else:
        raise RPCException(RPCException.ErrorCode.RegisterError, "{0}-{1}-{2}Service已经注册".format(ip, port,service_name))


def UnRegister(key: (str, str, str)):
    if __service.get(key, None) is not None:
        del __service[key]
        return True
    return False


def ClientRequestReceive(key: (str, str), token: BaseUserToken, request: ClientRequestModel):
    service: Service = __service.get((key[0], key[1], request.Service), None)
    if service is not None:
        method: classmethod = service.methods.get(request.MethodId, None)
        if method is not None:
            net_config: NetConfig = NetCore.Get(key)
            if net_config is not None:
                if net_config.OnInterceptor(service, method, token) and service.config.OnInterceptor(service, method,
                                                                                                     token):
                    if service.config.tokenEnable and request.Params.__len__() >= 1:
                        request.Params[0] = token
                        result = method.__cal___(request.Params)
                        return_name = service.config.type.abstractName.get(method.__annotations__["return"], None)
                        net_config.clientResponseSend(token, ClientResponseModel("2.0", json.dumps(result), return_name,
                                                                                 request.Id, request.Service, None))
            else:
                raise RPCException(RPCException.ErrorCode.RegisterError, "未找到NetConfig{0}".format(key))
        else:
            raise RPCException(RPCException.ErrorCode.RegisterError, "未找到方法{0}-{1}-{2}".format(key, request.Service, request.MethodId))
    else:
        raise RPCException(RPCException.ErrorCode.RegisterError, "未找到服务{0}-{1}".format(key, request.Service))
