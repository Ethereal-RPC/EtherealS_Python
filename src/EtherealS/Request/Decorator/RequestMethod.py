from EtherealS.Request.Decorator import InvokeTypeFlags


class RequestMethod:
    def __init__(self):
        self.invokeType = InvokeTypeFlags.Remote
        self.timeout = -1

    def __call__(self, func):
        func.__doc__ = self
        return func
