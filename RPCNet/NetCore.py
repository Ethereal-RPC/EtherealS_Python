import json

from Model.BaseUserToken import BaseUserToken
from Model.ClientRequestModel import ClientRequestModel
from Model.ClientResponseModel import ClientResponseModel
from Model.RPCException import RPCException
from RPCNet.NetConfig import NetConfig
from RPCService import ServiceCore
from RPCService.Service import Service

__cofigs = dict()


def Get(key: (str, str)) -> NetConfig:
    return __cofigs.get(key, None)


def RegisterByConfig(ip: str, port: str, config: NetConfig):
    key = (ip, port)
    if __cofigs.get(key, None) is None:
        config.clientRequestReceive = ClientRequestReceive
        __cofigs[key] = config
    else:
        raise RPCException(RPCException.ErrorCode.RegisterError, "{0}已注册，无法重复注册！".format(key))
    return __cofigs[key]


def GetTokens(key: (str, str)):
    config: NetConfig = __cofigs.get(key, None)
    if config is not None:
        return config.tokens


def ClientRequestReceive(key: (str, str), token: BaseUserToken, request: ClientRequestModel):
    service: Service = ServiceCore.GetByKey((key[0], key[1], request.Service))
    if service is not None:
        method: classmethod = service.methods.get(request.MethodId, None)
        if method is not None:
            net_config: NetConfig = Get(key)
            if net_config is not None:
                if net_config.OnInterceptor(service, method, token) and service.config.OnInterceptor(service, method,
                                                                                                     token):
                    if service.config.tokenEnable and request.Params.__len__() >= 1:
                        request.Params[0] = token
                    service.convert(request.MethodId, request.Params)
                    result = method.__call__(*request.Params)
                    return_type = method.__annotations__.get('return', None)
                    return_abstract_name = service.config.type.abstractName.get(return_type.__name__, None)
                    response = ClientResponseModel()
                    response.init("2.0", json.dumps(result), return_abstract_name, request.Id, request.Service, None)
                    net_config.clientResponseSend(token, response)
            else:
                raise RPCException(RPCException.ErrorCode.RegisterError, "未找到NetConfig{0}".format(key))
        else:
            raise RPCException(RPCException.ErrorCode.RegisterError, "未找到方法{0}-{1}-{2}".format(key, request.Service, request.MethodId))
    else:
        raise RPCException(RPCException.ErrorCode.RegisterError, "未找到服务{0}-{1}".format(key, request.Service))
