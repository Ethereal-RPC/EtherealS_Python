from abc import ABC, abstractmethod

from EtherealS.Core.BaseCore.MZCore import MZCore
from EtherealS.Core.Manager.AbstractType.AbstractType import AbstrackType
from EtherealS.Core.Model.TrackException import ExceptionCode, TrackException


def register(instance):
    for method_name in dir(instance):
        if not hasattr(instance, method_name):
            continue
        func = getattr(instance, method_name)
        if hasattr(func,"ethereal_requestMapping"):
            if func.__annotations__.__contains__("return"):
                parameterInfos = func.__annotations__
            else:
                raise TrackException(ExceptionCode.Core, "请定义{0}方法的返回值".format(func.ethereal_requestMapping.mapping))
            for (k,v) in parameterInfos.items():
                if k == "return":
                    continue
                elif instance.types.typesByType.get(v, None) is not None:
                    parameterInfos[k] = instance.types.typesByType.get(v, None)
                elif instance.types.typesByName.get(k, None) is not None:
                    parameterInfos[k] = instance.types.typesByName.get(k, None)
                if not isinstance(parameterInfos[k],AbstrackType):
                    raise TrackException(code=ExceptionCode.Core, message="{0}方法{1}参数对应的{2}类型的抽象类型尚未注册"
                                         .format(func.ethereal_requestMapping.mapping, k, parameterInfos[k]))
            from EtherealS.Request.Abstract import RequestInterceptor
            setattr(instance, method_name, RequestInterceptor.getInvoke(func))


class Request(ABC,MZCore):

    def __init__(self):
        MZCore.__init__(self)
        self.config = None
        self.name = None
        self.service = None

    @abstractmethod
    def Initialize(self):
        pass

    @abstractmethod
    def Register(self):
        pass

    @abstractmethod
    def UnRegister(self):
        pass

    @abstractmethod
    def UnInitialize(self):
        pass