from abc import ABC
from types import MethodType

from EtherealS.Core.Model.AbstractType import AbstrackType
from EtherealS.Core.Model.AbstractTypes import AbstractTypes
from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Core.Model.TrackLog import TrackLog
from EtherealS.Request.Abstract.RequestConfig import RequestConfig
from EtherealS.Core.Event import Event
from EtherealS.Request.Decorator.Request import RequestAnnotation


def register(instance):
    from EtherealS.Core.Model.TrackException import ExceptionCode, TrackException
    from EtherealS.Server.Abstract.BaseToken import BaseToken
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

                if types.__len__() == 0 or not issubclass(types[0], BaseToken):
                    raise TrackException(code=ExceptionCode.Core, message=
                    "{0}-{1}-{2}方法首参非BaseToken!".format(instance.net_name, instance.request_name,
                                                        func.__name__))

                if annotation.parameters is None:
                    for param in params[1::]:
                        if param is not None:
                            # annotations 有 module 有 class
                            rpc_type: AbstrackType = instance.types.typesByType.get(param, None)
                            if rpc_type is None:
                                raise TrackException(code=ExceptionCode.Core, message="对应的{0}类型的抽象类型尚未注册"
                                                     .format(param.__name__))
                            method_id += "-" + rpc_type.name
                else:
                    for abstract_name in annotation.parameters:
                        if instance.types.typesByName.get(abstract_name, None) is None:
                            raise TrackException(code=ExceptionCode.Core, message="对应的{0}抽象类型对应的实际类型尚未注册"
                                                 .format(abstract_name))
                        method_id += "-" + abstract_name

                invoke = instance.getInvoke(func=func, annotation=annotation, method_id=method_id)
                invoke.__annotations__ = func.__annotations__
                invoke.__doc__ = func.__doc__
                invoke.__name__ = func.__name__
                setattr(instance, method_name, invoke)


class Request(ABC):

    def __init__(self):
        self.config = None
        self.name = None
        self.net_name = None
        self.exception_event = Event()
        self.log_event = Event()
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

