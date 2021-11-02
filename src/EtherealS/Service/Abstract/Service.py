from abc import ABC, abstractmethod
from types import MethodType

from EtherealS.Core.Model.AbstractType import AbstrackType
from EtherealS.Core.Model.AbstractTypes import AbstractTypes
from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Core.Model.TrackLog import TrackLog
from EtherealS.Extension.Authority.IAuthoritable import IAuthoritable
from EtherealS.Core import Event


def register(service):
    for method_name in dir(service):
        func = getattr(service, method_name)
        from EtherealS.Service.Decorator.ServiceMethod import ServiceMethod
        if isinstance(func.__doc__, ServiceMethod):
            method_id = func.__name__
            if func.__annotations__.get("return") is not None:
                parameterInfos = list(func.__annotations__.values())[:-1:]
            else:
                raise TrackException(code=ExceptionCode.Core,
                                     message="%s-%s方法中的返回值未定义！".format(service, func.__name__))
            from EtherealS.Server.Abstract.Token import Token
            for parameterInfo in parameterInfos:
                if issubclass(parameterInfo, Token):
                    continue
                else:
                    abstractType: AbstrackType = service.types.typesByType.get(parameterInfo, None)
                    if abstractType is None:
                        raise TrackException(code=ExceptionCode.Core, message="对应的{0}类型的抽象类型尚未注册"
                                             .format(parameterInfo))
                    method_id += "-" + abstractType.name
            if service.methods.get(method_id, None) is not None:
                raise TrackException(code=ExceptionCode.Core, message="服务方法{name}已存在，无法重复注册！".format(name=method_id))
            service.methods[method_id] = func


class Service(ABC):
    def __init__(self):
        self.config = None
        self.methods = dict()
        self.net_name: str
        self.name = None
        self.exception_event: Event = Event.Event()
        self.log_event: Event = Event.Event()
        self.interceptorEvent = list()
        self.types = AbstractTypes()

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

    @abstractmethod
    def Initialize(self):
        pass

    @abstractmethod
    def UnInitialize(self):
        pass
