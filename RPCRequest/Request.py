import json
from types import MethodType

from Decorator.RPCRequest import RequestAnnotation
from Model.BaseUserToken import BaseUserToken
from Model.RPCException import RPCException, ErrorCode
from Model.ServerRequestModel import ServerRequestModel
from RPCNet import NetCore
from RPCRequest.RequestConfig import RequestConfig


class Request:

    def __init__(self, config: RequestConfig
                 ):
        self.config = config
        self.request_name: str = None
        self.server_key: (str, str) = None

    def register(self, instance, server_key: (str, str), request_name: str, config: RequestConfig):
        self.config = config
        self.server_key = server_key
        self.request_name = request_name
        for method_name in dir(instance):
            func = getattr(instance, method_name)
            if isinstance(func.__doc__, RequestAnnotation):
                assert isinstance(func, MethodType)
                annotation: RequestAnnotation = func.__doc__
                if annotation is not None:
                    method_id: str = func.__name__

                    types = list(func.__annotations__.values())
                    if func.__annotations__.get("return") is not None:
                        params = types[:-1:]
                    else:
                        params = types

                    if types.__len__() == 0 or not issubclass(types[0], BaseUserToken):
                        raise RPCException(ErrorCode.RegisterError,
                                           "{0}-{1}-{2}方法首参非BaseUserToken!".format(server_key, request_name,
                                                                                   func.__name__))

                    if annotation.paramters is None:
                        for param_type in params[1::]:
                            if param_type is not None:
                                abstract_name = self.config.type.abstractName.get(param_type.__name__, None)
                                if abstract_name is None:
                                    raise RPCException(ErrorCode.RegisterError,
                                                       "对应的{0}类型的抽象类型尚未注册".format(param_type.__name__))
                                method_id += "-" + abstract_name
                    else:
                        for abstract_name in annotation.paramters:
                            if self.config.type.abstractType.get(abstract_name, None) is None:
                                raise RPCException(ErrorCode.RegisterError,
                                                   "对应的{0}抽象类型对应的实际类型尚未注册".format(abstract_name))
                            method_id += "-" + abstract_name

                    def invoke(*args, **kwargs):
                        for param in args[1::]:
                            parameters = list()
                            parameters.append(json.dumps(param))
                            request = ServerRequestModel("2.0", method_id, parameters, request_name)
                            token = args.__getitem__(0)
                            if token is None:
                                raise RPCException(ErrorCode.NotFoundNetConfig,
                                                   "{0}-{1}-{2}方法BaseUserToken为None!".format(server_key, request_name,
                                                                                             func.__name__))
                            net_config = NetCore.Get(server_key)
                            if net_config is None:
                                raise RPCException(ErrorCode.NotFoundNetConfig,
                                                   "{0}-{1}-{2}方法在发送请求时，NetConfig为空！"
                                                   .format(server_key, request_name, request_name))
                            net_config.serverRequestSend(token, request)
                            return None

                    invoke.__annotations__ = func.__annotations__
                    invoke.__doc__ = func.__doc__
                    invoke.__name__ = func.__name__
                    setattr(instance, method_name, invoke)
