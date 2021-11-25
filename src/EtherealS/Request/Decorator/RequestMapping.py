from EtherealS.Request.Abstract import RequestInterceptor
from EtherealS.Request.Decorator import InvokeTypeFlags


class RequestMapping:
    def __init__(self,mapping,timeout=None,invokeType=InvokeTypeFlags.Remote):
        self.mapping = mapping
        self.timeout = timeout
        self.invokeType = invokeType

    def __call__(self, func):
        func = RequestInterceptor.getInvoke(func)
        func.ethereal_requestMapping = self
        return func
