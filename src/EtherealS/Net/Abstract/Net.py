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
        service: Service = self.services.get(request.Service)
        if service is not None:
            method: classmethod = service.methods.get(request.MethodId, None)
            if method is not None:
                if self.OnInterceptor(service, method, token) and service.OnInterceptor(self, method, token):
                    params_id = request.MethodId.split("-")
                    for i in range(1, params_id.__len__()):
                        rpc_type: AbstrackType = service.types.typesByName.get(params_id[i], None)
                        if rpc_type is None:
                            return ClientResponseModel(result=None, result_type=None, request_id=request.Id,
                                                       service=service,
                                                       error=Error(code=ErrorCode.NotFoundService,
                                                                   message="RPC中的{0}类型中尚未被注册".format(params_id[i])))
                        request.Params[i] = rpc_type.deserialize(request.Params[i])
                    if method.__annotations__.get("return") is not None:
                        params = list(method.__annotations__.values())[:-1:]
                    if params.__len__() == request.Params.__len__():
                        request.Params[0] = token
                    elif request.Params.__len__() > 1:
                        request.Params = request.Params[1::]
                    result = method.__call__(*request.Params)
                    return_type = method.__annotations__.get('return', None)
                    rpc_type = service.types.typesByType.get(return_type, None)
                    response = ClientResponseModel(result=rpc_type.serialize(result), result_type=rpc_type.name,
                                                   request_id=request.Id,
                                                   service=request.Service, error=None)
                    return response
            else:
                return ClientResponseModel(result=None, result_type=None, request_id=request.Id, service=service,
                                           error=Error(code=ErrorCode.NotFoundService,
                                                       message="未找到方法{0}-{1}-{2}".format(self.name, request.Service,
                                                                                         request.MethodId)))
        else:
            return ClientResponseModel(result=None, result_type=None, request_id=request.Id, service=service,
                                       error=Error(code=ErrorCode.NotFoundService,
                                                   message="未找到服务{0}-{1}".format(self.name, request.Service)))

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
