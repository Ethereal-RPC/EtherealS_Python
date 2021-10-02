from EtherealS.Core.Model.AbstractType import AbstrackType
from EtherealS.Core.Model.ServerRequestModel import ServerRequestModel
from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Request.Abstract.Request import Request
from EtherealS.Request.Decorator.Request import RequestAnnotation
from EtherealS.Request.WebSocket.WebSocketRequestConfig import WebSocketRequestConfig
from EtherealS.Server.Abstract.BaseToken import BaseToken


class WebSocketRequest(Request):

    def __init__(self):
        super().__init__()
        self.config = WebSocketRequestConfig()

    def getInvoke(self, func, method_id, annotation: RequestAnnotation):
        def invoke(*args, **kwargs):
            if args is None:
                raise TrackException(code=ExceptionCode.Runtime,
                                     message="{0}-{1}-{2}方法未提供首参BaseToken".format(self.net_name, self.name,
                                                                                  func.__name__))
            from EtherealS.Request.Decorator import InvokeTypeFlags
            localResult = None
            if (annotation.invokeType & InvokeTypeFlags.Local) == 0:
                parameters = list()
                for arg in args[1::]:
                    abstract_type: AbstrackType = self.types.typesByType.get(type(arg), None)
                    if abstract_type is None:
                        raise TrackException(code=ExceptionCode.Core, message="对应的{0}类型的抽象类型尚未注册"
                                             .format(arg.__name__))
                    parameters.append(abstract_type.serialize(arg))
                request = ServerRequestModel(method_id=method_id, params=parameters, service=self.name)
                token: BaseToken = args.__getitem__(0)
                if token is None:
                    raise TrackException(code=ExceptionCode.Core, message="{0}-{1}-{2}方法BaseToken为None!"
                                         .format(self.net_name, self.name, func.__name__))
                token.SendServerRequest(request)
                if (annotation.invokeType & InvokeTypeFlags.All) == 0:
                    localResult = func(*args, **kwargs)
                return None
            else:
                localResult = func(*args, **kwargs)
            return localResult

        return invoke
