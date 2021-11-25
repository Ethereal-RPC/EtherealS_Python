from abc import ABC, abstractmethod

from EtherealS.Core.BaseCore.MZCore import MZCore
from EtherealS.Core.Manager.AbstractType.AbstractType import AbstrackType
from EtherealS.Core.Manager.Event.Model.EventContext import EventContext
from EtherealS.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealS.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealS.Core.Model.Error import Error, ErrorCode
from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode


def register(instance):
    for method_name in dir(instance):
        if not hasattr(instance, method_name):
            continue
        func = getattr(instance, method_name)
        if hasattr(func,"ethereal_serviceMapping"):
            if func.__annotations__.__contains__("return"):
                parameterInfos = func.__annotations__
            else:
                raise TrackException(ExceptionCode.Core, "请定义{0}方法的返回值".format(func.ethereal_serviceMapping.mapping))
            for (k,v) in parameterInfos.items():
                if k == "return" and v is None:
                    continue
                from EtherealS.Service.Abstract.Token import Token
                if k == "token" and issubclass(v,Token):
                    continue
                elif instance.types.typesByType.get(v, None) is not None:
                    parameterInfos[k] = instance.types.typesByType.get(v, None)
                elif instance.types.typesByName.get(k, None) is not None:
                    parameterInfos[k] = instance.types.typesByName.get(k, None)
                if not isinstance(parameterInfos[k],AbstrackType):
                    raise TrackException(code=ExceptionCode.Core, message="{0}方法{1}参数对应的{2}类型的抽象类型尚未注册"
                                         .format(func.ethereal_serviceMapping.mapping, k, parameterInfos[k]))
            instance.methods[func.ethereal_serviceMapping.mapping] = func

class Service(ABC,MZCore):
    def __init__(self):
        MZCore.__init__(self)
        self.config = None
        self.methods = dict()
        self.net = None
        self.name = None
        self.requests = dict()
        self.tokens = dict()
        self.interceptorEvent = list()
        self.create_method = None

    def OnInterceptor(self, net, method, token) -> bool:
        for item in self.interceptorEvent:
            if not item.__call__(net, self, method, token):
                return False
        return True

    def ClientRequestReceiveProcess(self, token, request: ClientRequestModel):
        func: classmethod = self.methods.get(request.Mapping, None)
        if func is not None:
            if self.net.OnInterceptor(self, func, token) and self.OnInterceptor(self.net, func, token):
                result = None
                kwargs = dict()
                eventContext = EventContext()
                eventContext.method = func
                parameterInfos = func.__annotations__
                for k,v in func.__annotations__.items():
                    if k == "return":
                        continue
                    elif k == "token":
                        kwargs[k] = token
                        continue
                    kwargs[k] = v.deserialize(request.Params[k])
                if hasattr(func, "ethereal_beforeEvent"):
                    self.iocManager.InvokeEvent(func.ethereal_beforeEvent, kwargs, eventContext)
                try:
                    result = func(**kwargs)
                except Exception as e:
                    if hasattr(func, "ethereal_exceptionEvent"):
                        eventContext.exception = e
                        self.iocManager.InvokeEvent(func.ethereal_exceptionEvent, kwargs, eventContext)
                        if func.ethereal_exceptionEvent.isThrow:
                            raise e
                    else:
                        raise e
                if hasattr(func, "ethereal_afterEvent"):
                    eventContext.result = result
                    self.iocManager.InvokeEvent(func.ethereal_afterEvent, kwargs, eventContext)
                if func.__annotations__["return"] is not None:
                    rpc_type = func.__annotations__["return"]
                    return ClientResponseModel(result=rpc_type.serialize(result),id=request.Id, error=None)
                return None
        else:
            return ClientResponseModel(result=None, id=request.Id,
                                       error=Error(code=ErrorCode.NotFoundService,
                                                   message="未找到方法{0}-{1}".format(self.name, request.Mapping)))

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
