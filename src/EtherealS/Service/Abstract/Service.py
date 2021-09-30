from abc import ABC, abstractmethod
from types import MethodType

from EtherealS.Core.Model.AbstractType import AbstrackType
from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Core.Model.TrackLog import TrackLog
from EtherealS.Extension.Authority.IAuthoritable import IAuthoritable
from EtherealS.Service.Abstract import ServiceConfig
from EtherealS.Core import Event
from EtherealS.Service.Decorator.Service import ServiceAnnotation


def register(service):
    if service.config.authoritable and issubclass(service, IAuthoritable) is False:
        raise TrackException(code=ExceptionCode.Runtime, message="%s服务已开启权限系统，但尚未实现权限接口".format(service.__name__))
    for method_name in dir(service):
        func = getattr(service, method_name)
        if isinstance(func.__doc__, ServiceAnnotation):
            assert isinstance(func, MethodType)
            method_id = func.__name__
            if func.__doc__.paramters is None:

                if func.__annotations__.get("return") is not None:
                    params = list(func.__annotations__.values())[:-1:]
                else:
                    raise TrackException(code=ExceptionCode.Core,
                                         message="%s-%s方法中的返回值未定义！".format(net_name, func.__name__))
                start = 0
                from EtherealS.Server.WebSocket.WebSocketBaseToken import WebSocketBaseToken
                if params.__len__() > 0 and isinstance(params[0], type(WebSocketBaseToken)):
                    start = 1
                for param in params[start::]:
                    rpc_type: AbstrackType = service.types.typesByType.get(param, None)
                    if rpc_type is not None:
                        method_id = method_id + "-" + rpc_type.name
                    else:
                        raise TrackException(code=ExceptionCode.Core, message="{name}方法中的{param}类型参数尚未注册"
                                             .format(name=func.__name__, param=param.__name__))
            else:
                for param in func.__doc__.paramters:
                    rpc_type: AbstrackType = service.types.abstractType.get(type(param), None)
                    if rpc_type is not None:
                        method_id = method_id + "-" + rpc_type.name
                    else:
                        raise TrackException(code=ExceptionCode.Core,
                                             message="%s方法中的%s抽象类型参数尚未注册".format(func.__name__, param))
            if service.methods.get(method_id, None) is not None:
                raise TrackException(code=ExceptionCode.Core, message="服务方法{name}已存在，无法重复注册！".format(name=method_id))
            service.methods[method_id] = func


class Service(ABC):
    def __init__(self, name, types):
        self.config = None
        self.methods = dict()
        self.net_name: str
        self.name = name
        self.exception_event: Event = Event.Event()
        self.log_event: Event = Event.Event()
        self.interceptorEvent = list()
        self.types = types

    def OnLog(self, log: TrackLog = None, code=None, message=None):
        if log is None:
            log = TrackLog(code=code, message=message)
        log.server = self
        self.log_event.OnEvent(log=log)

    def OnException(self, exception: TrackException = None, code=None, message=None):
        if exception is None:
            exception = TrackException(code=code, message=message)
        exception.server = self
        self.exception_event.OnEvent(exception=exception)

    def OnInterceptor(self, net, method, token) -> bool:
        for item in self.interceptorEvent:
            if not item.__call__(net, self, method, token):
                return False
        return True
