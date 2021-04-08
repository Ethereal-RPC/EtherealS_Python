def RPCService_2(timeout):
    def getFunc(func):
        def Func(*args, **kwargs):
            func(*args, **kwargs)
        annotation = ServiceAnnotation()
        annotation.timeout = timeout
        Func.__doc__ = annotation
        return Func
    return getFunc


def RPCService_3(paramters, timeout):
    def getFunc(func):
        def Func(*args, **kwargs):
            func(*args, **kwargs)
        annotation = ServiceAnnotation()
        annotation.timeout = timeout
        annotation.paramters = paramters
        Func.__doc__ = annotation
        return Func
    return getFunc


def RPCService_1(paramters):
    def getFunc(func):
        def Func(*args, **kwargs):
            func(*args, **kwargs)
        annotation = ServiceAnnotation()
        annotation.paramters = paramters
        Func.__doc__ = annotation
        return Func
    return getFunc


class ServiceAnnotation:
    timeout = -1
    paramters = None
