from EtherealS.Request.Decorator import InvokeTypeFlags


class Service:
    def __init__(self):
        pass
    
    def __call__(self, func):
        func.__doc__ = self
        return func
