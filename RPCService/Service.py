import inspect
import json
import modulefinder
from types import MethodType

from Model.RPCLog import RPCLog
from Model.RPCType import RPCType
from RPCService import ServiceConfig
from Decorator.RPCService import ServiceAnnotation
from Extension.Authority.IAuthoritable import IAuthoritable
from Model import RPCException
from Model.BaseUserToken import BaseUserToken
from Model.RPCException import ErrorCode
from Utils import JsonTool
from Utils import Event


class Service:
    def __init__(self):
        self.config: ServiceConfig = None
        self.methods = dict()
        self.instance = None
        self.net_name = None
        self.service_name = None
        self.exception_event: Event = Event.Event()
        self.log_event: Event = Event.Event()

    def register(self, net_name, service_name, instance, config: ServiceConfig):
        self.config: ServiceConfig = config
        self.instance = instance
        self.net_name = net_name
        self.service_name = service_name
        if config.authoritable and issubclass(instance, IAuthoritable) is False:
            self.OnException(code=ErrorCode.Runtime, message="%s服务已开启权限系统，但尚未实现权限接口".format(instance.__name__),
                             service=self)
        for method_name in dir(instance):
            func = getattr(instance, method_name)
            if isinstance(func.__doc__, ServiceAnnotation):
                assert isinstance(func, MethodType)
                method_id = func.__name__
                if func.__doc__.paramters is None:

                    if func.__annotations__.get("return") is not None:
                        params = list(func.__annotations__.values())[:-1:]
                    else:
                        self.OnException(code=ErrorCode.Core, message="%s-%s方法中的返回值未定义！"
                                         .format(net_name, func.__name__), service=self)
                    start = 0
                    if params.__len__() > 0 and isinstance(params[0], BaseUserToken) and func.__doc__.token:
                        start = 1
                    for param in params[start::]:
                        rpc_type: RPCType = self.config.types.typesByType.get(param, None)
                        if rpc_type is not None:
                            method_id = method_id + "-" + rpc_type.name
                        else:
                            self.OnException(code=ErrorCode.Core, message="{name}方法中的{param}类型参数尚未注册"
                                             .format(name=func.__name__, param=param.__name__), service=self)
                else:
                    for param in func.__doc__.paramters:
                        rpc_type: RPCType = self.config.types.abstractType.get(type(param), None)
                        if rpc_type is not None:
                            method_id = method_id + "-" + rpc_type.name
                        else:
                            self.OnException(code=ErrorCode.Core,
                                             message="%s方法中的%s抽象类型参数尚未注册".format(func.__name__, param), service=self)
                if self.methods.get(method_id, None) is not None:
                    self.OnException(code=ErrorCode.Core, message="服务方法{name}已存在，无法重复注册！".format(name=method_id),
                                     service=self)
                self.methods[method_id] = func

    def OnLog(self, **kwargs):
        code = kwargs.get("code")
        message = kwargs.get("message")
        service = kwargs.get("service")
        log = kwargs.get("log")
        if log is None:
            log = RPCLog(code, message)
        self.log_event.OnEvent(log=log, service=service)

    def OnException(self, **kwargs):
        code = kwargs.get("code")
        message = kwargs.get("message")
        exception = kwargs.get("exception")
        service = kwargs.get("service")
        if exception is None:
            exception = RPCException.RPCException(code, message)
        self.exception_event.OnEvent(exception=exception, service=service)
        raise exception
