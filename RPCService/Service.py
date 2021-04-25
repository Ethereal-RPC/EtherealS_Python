import json
from types import MethodType

from Model.RPCType import RPCType
from RPCService import ServiceConfig
from Decorator.RPCService import ServiceAnnotation
from Extension.Authority.IAuthoritable import IAuthoritable
from Model import RPCException
from Model.BaseUserToken import BaseUserToken
from Model.RPCException import ErrorCode
from Utils import JsonTool


class Service:
    def __init__(self):
        self.config: ServiceConfig = None
        self.methods = dict()
        self.instance = None
        self.key = None
        self.service_name = None

    def register(self, key, service_name, instance, config: ServiceConfig):
        self.config: ServiceConfig = config
        self.instance = instance
        self.key = key
        self.service_name = service_name
        if config.authoritable and issubclass(instance, IAuthoritable) is False:
            raise RPCException.RPCException(ErrorCode.RegisterError,
                                            "{0} 服务已开启权限系统，但尚未实现权限接口".format(instance.__name__))
        for method_name in dir(instance):
            func = getattr(instance, method_name)
            if isinstance(func.__doc__, ServiceAnnotation):
                assert isinstance(func, MethodType)
                method_id = func.__name__
                if func.__doc__.paramters is None:

                    if func.__annotations__.get("return") is not None:
                        params = list(func.__annotations__.values())[:-1:]
                    else:
                        raise RPCException.RPCException(ErrorCode.RegisterError,
                                                        "{1}-{0}方法中的返回值为定义！".format(func.__name__, key))
                    start = 0
                    if params.__len__() > 0 and isinstance(params[0], BaseUserToken) and func.__doc__.token:
                        start = 1
                    for param_name in params[start::]:
                        rpc_type: RPCType = self.config.types.typesByType.get(type(param_name), None)
                        if rpc_type is not None:
                            method_id = method_id + "-" + rpc_type.name
                        else:
                            raise RPCException.RPCException(ErrorCode.RegisterError,
                                                            "{0}方法中的{1}类型参数尚未注册".format(func.__name__,
                                                                                        param_name.__name__))
                else:
                    for param in func.__doc__.paramters:
                        rpc_type: RPCType = self.config.types.abstractType.get(param, None)
                        if rpc_type is not None:
                            method_id = method_id + "-" + rpc_type.name
                        else:
                            raise RPCException.RPCException(ErrorCode.RegisterError,
                                                            "{0}方法中的{1}抽象类型参数尚未注册".format(func.__name__,
                                                                                          param))
                if self.methods.get(method_id, None) is not None:
                    raise RPCException.RPCException(ErrorCode.RegisterError,
                                                    "服务方法{name}已存在，无法重复注册！".format(name=method_id))
                self.methods[method_id] = func
