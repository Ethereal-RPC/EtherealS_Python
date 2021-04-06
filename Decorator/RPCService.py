def RPCService(timeout):
    def getFunc(func):
        def Func(*args, **kwargs):
            func(*args, **kwargs)
        annotation = ServiceAnnotation()
        annotation.timeout = timeout
        Func.__doc__ = annotation
        return Func
    return getFunc


def RPCService(paramters, timeout):
    def getFunc(func):
        def Func(*args, **kwargs):
            func(*args, **kwargs)
        annotation = ServiceAnnotation()
        annotation.timeout = timeout
        annotation.paramters = paramters
        Func.__doc__ = annotation
        return Func
    return getFunc


class ServiceAnnotation:
    timeout = None
    paramters = None
