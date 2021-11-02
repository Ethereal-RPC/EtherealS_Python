from abc import ABC, abstractmethod
from enum import Enum

from EtherealS.Core.Model import ClientRequestModel
from EtherealS.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealS.Core.Model.Error import Error, ErrorCode
from EtherealS.Core.Model.TrackException import TrackException
from EtherealS.Core.Model.TrackLog import TrackLog
from EtherealS.Core.Model.AbstractType import AbstrackType
from EtherealS.Server.Abstract import Server
from EtherealS.Net.Abstract.NetConfig import NetConfig
from EtherealS.Server.Abstract.Token import Token
from EtherealS.Service.Abstract.Service import Service
from EtherealS.Core.Event import Event


class NetType(Enum):
    WebSocket = 1


class Net(ABC):
    def __init__(self, name, config):
        self.tokens = dict()
        self.name = name
        self.server: Server = None
        self.config: NetConfig = config
        self.services = dict()
        self.requests = dict()
        self.exception_event = Event()
        self.log_event = Event()
        self.interceptorEvent = list()
        self.type = None

    def ClientRequestReceiveProcess(self, token, request: ClientRequestModel):
        service: Service = self.services.get(request.ServiceMethod)
        if service is not None:
            method: classmethod = service.methods.get(request.MethodId, None)
            if method is not None:
                if self.OnInterceptor(service, method, token) and service.OnInterceptor(self, method, token):
                    parameters = list()
                    parameterInfos = list(method.__annotations__.values())[:-1:]
                    i = 0
                    for parameterInfo in parameterInfos:
                        if issubclass(parameterInfo, Token):
                            parameters.append(token)
                        else:
                            abstractType: AbstrackType = service.types.typesByType.get(parameterInfo, None)
                            parameters.append(abstractType.deserialize(request.Params[i]))
                            i = i + 1
                    result = method.__call__(*parameters)
                    return_type = method.__annotations__.get('return', None)
                    rpc_type = service.types.typesByType.get(return_type, None)
                    response = ClientResponseModel(result=rpc_type.serialize(result),
                                                   request_id=request.Id,
                                                   service=request.ServiceMethod, error=None)
                    return response
            else:
                return ClientResponseModel(result=None, request_id=request.Id, service=service,
                                           error=Error(code=ErrorCode.NotFoundService,
                                                       message="未找到方法{0}-{1}-{2}".format(self.name, request.ServiceMethod,
                                                                                         request.MethodId)))
        else:
            return ClientResponseModel(result=None, request_id=request.Id, service=service,
                                       error=Error(code=ErrorCode.NotFoundService,
                                                   message="未找到服务{0}-{1}".format(self.name, request.ServiceMethod)))

    @abstractmethod
    def Publish(self):
        pass

    def OnLog(self, log: TrackLog = None, code=None, message=None):
        if log is None:
            log = TrackLog(code=code, message=message)
        log.server = self
        self.log_event.OnEvent(log=log)

    def OnException(self, exception: TrackException = None, code=None, message=None):
        if exception is None:
            exception = TrackException(code=code, message=message)
        exception.server = self
        self.exception_event.OnEvent(exception=exception)

    def OnInterceptor(self, service: Service, method, token) -> bool:
        for item in self.interceptorEvent:
            if not item.__call__(self, service, method, token):
                return False
        return True
