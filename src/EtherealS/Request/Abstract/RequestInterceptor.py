import sys

from EtherealS.Core.Manager.AbstractType.AbstractType import AbstrackType
from EtherealS.Core.Manager.Event.Model.EventContext import EventContext
from EtherealS.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealS.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Request.Abstract.Request import Request
from EtherealS.Service.Abstract.Token import Token


def getInvoke(func):
    def invoke(self:Request,*args,**kwargs):
        from EtherealS.Request.Decorator import InvokeTypeFlags
        from EtherealS.Request.Decorator.RequestMapping import RequestMapping
        requestMapping: RequestMapping = func.ethereal_requestMapping
        requestModel = ClientRequestModel(mapping=requestMapping.mapping)
        localResult = None
        eventContext = EventContext()
        eventContext.method = func
        if hasattr(func,"ethereal_beforeEvent"):
            self.iocManager.InvokeEvent(func.ethereal_beforeEvent,kwargs,eventContext)
        keys = list(func.__annotations__.keys())
        for i in range(args.__len__()):
            kwargs[keys[i]] = args[i]
        token : Token= kwargs["token"]
        if token is None or not isinstance(token,Token):
            raise TrackException(code=ExceptionCode.Runtime,
                                 message="服务器请求{0}中的{1}方法未提供Token参数".format(self.name,func.__name__))
        if requestMapping.invokeType & InvokeTypeFlags.Local != 0:
            try:
                localResult = func(self,**kwargs)
            except Exception as e:
                if hasattr(func, "ethereal_exceptionEvent"):
                    eventContext.exception = e
                    self.iocManager.InvokeEvent(func.ethereal_exceptionEvent, kwargs, eventContext)
                    if func.ethereal_exceptionEvent.isThrow:
                        raise e
                else:
                    raise e
        if hasattr(func, "ethereal_afterEvent"):
            eventContext.result = localResult
            self.iocManager.InvokeEvent(func.ethereal_afterEvent,kwargs,eventContext)
        if requestMapping.invokeType & InvokeTypeFlags.Remote != 0:
            for v,k in func.__annotations__.items():
                if v == "return":
                    continue
                elif v == "token":
                    continue
                requestModel.Params[v] = k.serialize(kwargs[v])
            token.SendServerRequest(requestModel)
        return localResult
    invoke.__dict__ = func.__dict__
    invoke.__name__ = func.__name__
    invoke.__annotations__ = func.__annotations__
    return invoke
