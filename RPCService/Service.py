from types import MethodType

from Decorator.RPCService import ServiceAnnotation
from Extension.Authority.IAuthoritable import IAuthoritable
from Model import RPCException
from Model.BaseUserToken import BaseUserToken
from Model.RPCException import ErrorCode
from RPCService.ServiceConfig import ServiceConfig


class Service:
    config = None
    methods = dict()
    paramStart = None
    instance = None

    def register(self, instance, config: ServiceConfig):
        self.config = config
        self.instance = instance
        if config.tokenEnable:
            self.paramStart = 1
        else:
            self.paramStart = 0
        if config.authoritable and issubclass(instance, IAuthoritable) is False:
            raise RPCException.RPCException(ErrorCode.RegisterError,
                                            "{0} 服务已开启权限系统，但尚未实现权限接口".format(instance.__name__))
        for method_name in dir(instance):
            func = getattr(instance, method_name)
            if isinstance(func.__doc__, ServiceAnnotation):
                assert isinstance(func, MethodType)
                method_id = func.__name__
                if func.__doc__.paramters is None:
                    params = list(func.__annotations__.values())
                    if self.paramStart == 1 and issubclass(params[0], BaseUserToken):
                        raise RPCException.RPCException(ErrorCode.RegisterError,
                                                        "{0}方法中的首参数并非继承于BaseUserToken!".format(func.__name__))
                    method_id.join(func.__name__)
                    for param_name in params[self.paramStart::]:
                        abstract_name = self.config.type.abstractName.get(param_name.__name__, None)
                        if abstract_name is not None:
                            method_id.join("-").join(param_name)
                        else:
                            raise RPCException.RPCException(ErrorCode.RegisterError,
                                                            "{0}方法中的{1}类型参数尚未注册".format(func.__name__,
                                                                                        param_name.__name__))
                else:
                    for param in func.__doc__.paramters:
                        abstract_name = self.config.type.abstractType.get(param.__name__, None)
                        if abstract_name is not None:
                            method_id.join("-").join(param.__name__)
                        else:
                            raise RPCException.RPCException(ErrorCode.RegisterError,
                                                            "{0}方法中的{1}抽象类型参数尚未注册".format(func.__name__,
                                                                                          param.__name__))
                if self.methods[method_id] is not None:
                    raise RPCException.RPCException(ErrorCode.RegisterError,
                                                    "服务方法{name}已存在，无法重复注册！".format(name=method_id))
                self.methods[method_id] = func
