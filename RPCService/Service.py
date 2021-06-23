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
        self.net_name = None
        self.service_name = None

    def register(self, net_name, service_name, instance, config: ServiceConfig):
        self.config: ServiceConfig = config
        self.instance = instance
        self.net_name = net_name
        self.service_name = service_name
        if config.authoritable and issubclass(instance, IAuthoritable) is False:
            self.config.OnLog(RPCException.RPCException(ErrorCode.Core,
                                                        "{0} 服务已开启权限系统，但尚未实现权限接口"
                                                        .format(instance.__name__)), service=self)
        for method_name in dir(instance):
            func = getattr(instance, method_name)
            if isinstance(func.__doc__, ServiceAnnotation):
                assert isinstance(func, MethodType)
                method_id = func.__name__
                if func.__doc__.paramters is None:

                    if func.__annotations__.get("return") is not None:
                        params = list(func.__annotations__.values())[:-1:]
                    else:
                        self.config.OnException(code=ErrorCode.Core, message="{1}-{0}方法中的返回值未定义！"
                                                .format(net_name, func.__name__), service=self)
                    start = 0
                    if params.__len__() > 0 and isinstance(params[0], BaseUserToken) and func.__doc__.token:
                        start = 1
                    for param_name in params[start::]:
                        rpc_type: RPCType = self.config.types.typesByType.get(type(param_name), None)
                        if rpc_type is not None:
                            method_id = method_id + "-" + rpc_type.name
                        else:
                            self.config.OnException(code=ErrorCode.Core, message="{0}方法中的{1}类型参数尚未注册"
                                                    .format(func.__name__, param_name.__name__), service=self)
                else:
                    for param in func.__doc__.paramters:
                        rpc_type: RPCType = self.config.types.abstractType.get(param, None)
                        if rpc_type is not None:
                            method_id = method_id + "-" + rpc_type.name
                        else:
                            self.config.OnException(code=ErrorCode.Core, message="{0}方法中的{1}抽象类型参数尚未注册"
                                                    .format(func.__name__, param), service=self)
                if self.methods.get(method_id, None) is not None:
                    self.config.OnException(code=ErrorCode.Core, message="服务方法{name}已存在，无法重复注册！"
                                            .format(name=method_id), service=self)
                self.methods[method_id] = func
