from types import MethodType

from Core.Model.TrackException import TrackException,ExceptionCode
from Service.Abstract.Service import Service
from Service.Decorator.Service import ServiceAnnotation
from Extension.Authority.IAuthoritable import IAuthoritable
from Core.Model import TrackException
from Core.Model import TrackLog
from Core.Model.AbstractType import AbstrackType
from Service.Abstract import ServiceConfig


class WebSocketService(Service):
    def __init__(self):
        super().__init__()

    def register(self, net_name, service_name, instance, config: ServiceConfig):
        self.config: ServiceConfig = config
        self.instance = instance
        self.net_name = net_name
        self.service_name = service_name
        if config.authoritable and issubclass(instance, IAuthoritable) is False:
            raise TrackException(code=ExceptionCode.Runtime, message="%s服务已开启权限系统，但尚未实现权限接口".format(instance.__name__))
        for method_name in dir(instance):
            func = getattr(instance, method_name)
            if isinstance(func.__doc__, ServiceAnnotation):
                assert isinstance(func, MethodType)
                method_id = func.__name__
                if func.__doc__.paramters is None:

                    if func.__annotations__.get("return") is not None:
                        params = list(func.__annotations__.values())[:-1:]
                    else:
                        raise TrackException(code=ExceptionCode.Core,
                                             message="%s-%s方法中的返回值未定义！".format(net_name, func.__name__))
                    start = 0
                    from Server.WebSocket.WebSocketBaseToken import WebSocketBaseToken
                    if params.__len__() > 0 and isinstance(params[0], type(WebSocketBaseToken)):
                        start = 1
                    for param in params[start::]:
                        rpc_type: AbstrackType = self.config.types.typesByType.get(param, None)
                        if rpc_type is not None:
                            method_id = method_id + "-" + rpc_type.name
                        else:
                            raise TrackException(code=ExceptionCode.Core, message="{name}方法中的{param}类型参数尚未注册"
                                                 .format(name=func.__name__, param=param.__name__))
                else:
                    for param in func.__doc__.paramters:
                        rpc_type: AbstrackType = self.config.types.abstractType.get(type(param), None)
                        if rpc_type is not None:
                            method_id = method_id + "-" + rpc_type.name
                        else:
                            raise TrackException(code=ExceptionCode.Core,
                                                 message="%s方法中的%s抽象类型参数尚未注册".format(func.__name__, param))
                if self.methods.get(method_id, None) is not None:
                    raise TrackException(code=ExceptionCode.Core, message="服务方法{name}已存在，无法重复注册！".format(name=method_id))
                self.methods[method_id] = func
