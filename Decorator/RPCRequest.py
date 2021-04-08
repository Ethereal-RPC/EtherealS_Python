def RPCRequest_1(paramters):
    def getFunc(func):
        def Func(*args, **kwargs):
            func(*args, **kwargs)
        annotation = RequestAnnotation()
        annotation.paramters = paramters
        Func.__doc__ = annotation
        return Func
    return getFunc


class RequestAnnotation:
    paramters = None
