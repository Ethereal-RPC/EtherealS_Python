from Model.ClientRequestModel import ClientRequestModel
from Model.ClientResponseModel import ClientResponseModel
from Model.Error import Error, ErrorCode
from Model.RPCException import RPCException
from Model.RPCLog import RPCLog
from Model.RPCType import RPCType
from Model.RPCTypeConfig import RPCTypeConfig
from NativeServer import SocketListener
from RPCNet.NetConfig import NetConfig
from RPCService.Service import Service
from Utils.Event import Event


class Net:
    def __init__(self):
        self.tokens = dict()
        self.clientRequestReceive = self.ClientRequestReceiveProcess
        self.name: str = None
        self.server: SocketListener = None
        self.config: NetConfig = None
        self.services = dict()
        self.requests = dict()
        self.exception_event = Event()
        self.log_event = Event()

    def ClientRequestReceiveProcess(self, token, request: ClientRequestModel):
        service: Service = self.services.get(request.Service)
        if service is not None:
            method: classmethod = service.methods.get(request.MethodId, None)
            if method is not None:
                if service.config.OnInterceptor(service, method, token) and service.config.OnInterceptor(service,
                                                                                                         method,
                                                                                                         token):
                    params_id = request.MethodId.split("-")
                    for i in range(1, params_id.__len__()):
                        rpc_type: RPCType = service.config.types.typesByName.get(params_id[i], None)
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
                    rpc_type = service.config.types.typesByType.get(return_type, None)
                    response = ClientResponseModel(result=rpc_type.serialize(result), rpc_type=rpc_type.name,
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

    def Publish(self):
        if self.config.netNodeMode:
            types: RPCTypeConfig = RPCTypeConfig()

        self.server.start()
        return True

    def OnLog(self, **kwargs):
        code = kwargs.get("code")
        message = kwargs.get("message")
        net = kwargs.get("net")
        log = kwargs.get("log")
        if log is None:
            log = RPCLog(code, message)
        self.log_event.OnEvent(log=log, net=net)

    def OnException(self, **kwargs):
        code = kwargs.get("code")
        message = kwargs.get("message")
        exception = kwargs.get("exception")
        if exception is None:
            exception = RPCException(code, message)
        self.exception_event.OnEvent(exception=exception, net=self)
