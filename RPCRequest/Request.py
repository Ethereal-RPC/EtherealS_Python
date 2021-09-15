from types import MethodType

from Decorator.RPCRequest import RequestAnnotation
from Model.RPCException import RPCException, ExceptionCode
from Model.RPCLog import RPCLog
from Model.RPCType import RPCType
from Model.ServerRequestModel import ServerRequestModel
from RPCRequest.RequestConfig import RequestConfig
from Utils.Event import Event


class Request:

    def __init__(self, config: RequestConfig):
        self.config = config
        self.name = None
        self.net_name = None
        self.exception_event = Event()
        self.log_event = Event()

    def register(self, instance, net_name, request_name: str, config: RequestConfig):
        from NativeServer.BaseToken import BaseToken
        self.config = config
        self.net_name = net_name
        self.name = request_name
        for method_name in dir(instance):
            func = getattr(instance, method_name)
            if isinstance(func.__doc__, RequestAnnotation):
                assert isinstance(func, MethodType)
                annotation: RequestAnnotation = func.__doc__
                if annotation is not None:
                    method_id: str = func.__name__

                    types = list(func.__annotations__.values())
                    if func.__annotations__.get("return") is not None:
                        params = types[:-1:]
                    else:
                        params = types

                    if types.__len__() == 0 or not issubclass(types[0], BaseToken):
                        raise RPCException(code=ExceptionCode.Core, message=
                        "{0}-{1}-{2}方法首参非BaseToken!".format(net_name, request_name,
                                                            func.__name__))

                    if annotation.paramters is None:
                        for param in params[1::]:
                            if param is not None:
                                # annotations 有 module 有 class
                                rpc_type: RPCType = self.config.types.typesByType.get(param, None)
                                if rpc_type is None:
                                    raise RPCException(code=ExceptionCode.Core, message="对应的{0}类型的抽象类型尚未注册"
                                                       .format(param.__name__))
                                method_id += "-" + rpc_type.name
                    else:
                        for abstract_name in annotation.paramters:
                            if self.config.types.typesByName.get(abstract_name, None) is None:
                                raise RPCException(code=ExceptionCode.Core, message="对应的{0}抽象类型对应的实际类型尚未注册"
                                                   .format(abstract_name))
                            method_id += "-" + abstract_name

                    def invoke(*args, **kwargs):
                        for param in args[1::]:
                            parameters = list()
                            rpc_type: RPCType = self.config.types.typesByType.get(type(param), None)
                            if rpc_type is None:
                                raise RPCException(code=ExceptionCode.Core, message="对应的{0}类型的抽象类型尚未注册"
                                                   .format(param.__name__))
                            parameters.append(rpc_type.serialize(param))
                            request = ServerRequestModel(method_id, parameters, request_name)
                            token: BaseToken = args.__getitem__(0)
                            if token is None:
                                raise RPCException(code=ExceptionCode.Core, message="{0}-{1}-{2}方法BaseToken为None!"
                                                   .format(net_name, request_name, func.__name__))
                            token.SendServerRequest(request)
                            return None

                    invoke.__annotations__ = func.__annotations__
                    invoke.__doc__ = func.__doc__
                    invoke.__name__ = func.__name__
                    setattr(instance, method_name, invoke)

    def OnLog(self, **kwargs):
        code = kwargs.get("code")
        message = kwargs.get("message")
        request = kwargs.get("request")
        log = kwargs.get("log")
        if log is None:
            log = RPCLog(code, message)
        self.log_event.OnEvent(log=log, request=request)

    def OnException(self, **kwargs):
        code = kwargs.get("code")
        message = kwargs.get("message")
        exception = kwargs.get("exception")
        if exception is None:
            exception = RPCException(code, message)
        self.exception_event.OnEvent(exception=exception, request=self)
