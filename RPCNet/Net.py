from Model.BaseUserToken import BaseUserToken
from Model.ClientRequestModel import ClientRequestModel
from Model.ClientResponseModel import ClientResponseModel
from Model.RPCException import RPCException, ErrorCode
from Model.RPCType import RPCType
from NativeServer import SocketListener
from RPCNet.NetConfig import NetConfig
from RPCService.Service import Service


class Net:
    def __init__(self):
        self.tokens = dict()
        self.clientRequestReceive = self.ClientRequestReceiveProcess
        self.serverRequestSend = None
        self.clientResponseSend = None
        self.name: str = None
        self.server: SocketListener = None
        self.config: NetConfig = None
        self.services = dict()
        self.requests = dict()

    def ClientRequestReceiveProcess(self, token: BaseUserToken, request: ClientRequestModel):
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
                            raise RPCException(ErrorCode.Core, "RPC中的{0}类型中尚未被注册"
                                               .format(params_id[i]))
                        params_id[i] = rpc_type.deserialize(params_id[i])
                    if method.__annotations__.__len__() == request.Params.__len__():
                        request.Params[0] = token
                    elif request.Params.__len__() > 1:
                        request.Params = request.Params[1::]
                    result = method.__call__(*request.Params)
                    return_type = method.__annotations__.get('return', None)
                    rpc_type = service.config.types.typesByType.get(type(return_type), None)
                    response = ClientResponseModel()
                    response.init("2.0", rpc_type.serialize(result), rpc_type.name, request.Id, request.Service,
                                  None)
                    self.clientResponseSend(token, response)
            else:
                raise RPCException(ErrorCode.Core,
                                   "未找到方法{0}-{1}-{2}".format(self.name, request.Service, request.MethodId))
        else:
            self.config.OnException(exception=RPCException(ErrorCode.Core, "未找到服务{0}-{1}".format(self.name, request.Service)), net=self)
