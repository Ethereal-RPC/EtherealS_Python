from EtherealS.Core.Model.AbstractType import AbstrackType
from EtherealS.Core.Model.ServerRequestModel import ServerRequestModel
from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Request.Abstract.Request import Request
from EtherealS.Request.WebSocket.WebSocketRequestConfig import WebSocketRequestConfig
from EtherealS.Server.Abstract.Token import Token


class WebSocketRequest(Request):

    def __init__(self):
        super().__init__()
        self.config = WebSocketRequestConfig()

    def getInvoke(self, func, annotation):

        def invoke(*args, **kwargs):
            from EtherealS.Request.Decorator import InvokeTypeFlags
            localResult = None
            if (annotation.invokeType & InvokeTypeFlags.Local) == 0:
                method_id: str = func.__name__
                params = list()
                if func.__annotations__.get("return") is not None:
                    parameterInfos = list(func.__annotations__.values())[:-1:]
                else:
                    parameterInfos: list = list(func.__annotations__.values())
                token = None
                for i in range(0, parameterInfos.__len__()):
                    if issubclass(parameterInfos[i], Token):
                        token = args[i]
                    else:
                        abstractType: AbstrackType = self.types.typesByType.get(parameterInfos[i], None)
                        if abstractType is None:
                            raise TrackException(code=ExceptionCode.Core, message="对应的{0}类型的抽象类型尚未注册"
                                                    .format(parameterInfos[i]))
                        method_id += "-" + abstractType.name
                        params.append(abstractType.serialize(args[i]))
                request = ServerRequestModel(method_id=method_id, params=params, service=self.name)
                if token is None:
                    raise TrackException(code=ExceptionCode.Core, message="{0}-{1}-{2}方法Token为None!"
                                         .format(self.net_name, self.name, func.__name__))
                token.SendServerRequest(request)
                if (annotation.invokeType & InvokeTypeFlags.All) == 0:
                    localResult = func(*args, **kwargs)
                return None
            else:
                localResult = func(*args, **kwargs)
            return localResult

        return invoke
