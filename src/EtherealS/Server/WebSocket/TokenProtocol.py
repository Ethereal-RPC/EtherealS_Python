import autobahn
from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.websocket import protocol

from EtherealS.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealS.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealS.Core.Model.Error import ErrorCode, Error
from EtherealS.Core.Model.ServerRequestModel import ServerRequestModel
from EtherealS.Core.Model.TrackLog import LogCode
from EtherealS.Service import ServiceCore
from EtherealS.Service.Abstract import ServiceConfig


class TokenProtocol(WebSocketServerProtocol):

    def __init__(self,net_name):
        WebSocketServerProtocol.__init__(self)
        self.token = None
        self.net_name = net_name

    def processHandshake(self):
        # only proceed when we have fully received the HTTP request line and all headers
        #
        end_of_header = self.data.find(b"\x0d\x0a\x0d\x0a")
        if end_of_header >= 0:

            http_request_data = self.data[:end_of_header + 4]
            body_raw = self.data[end_of_header + 4:]

            # extract HTTP status line and headers
            #
            try:
                http_status_line, http_headers, http_headers_cnt = \
                    protocol.parseHttpHeader(http_request_data)
            except Exception as e:
                return self.failHandshake("Error during parsing of HTTP status line / request headers : {0}".format(e))

            # HTTP RequestMapping line : METHOD, VERSION
            #
            rl = http_status_line.split()
            paths = rl[1].split("/")
            if paths.__len__() == 0:
                self.SendHttpError(code=ErrorCode.Common, message="URL格式错误", request=None)
            if paths[-1] == "":
                service_name = paths[-2]
            else:
                service_name = paths[-1]
            service = ServiceCore.Get(service_name=service_name, net_name=self.net_name)
            if service is None:
                self.SendHttpError(code=ErrorCode.Common, message="{0}服务未找到".format(service_name), request=None)
            self.token = service.create_method()
            self.token.service = service
            self.token.log_event.Register(service.OnLog)
            self.token.exception_event.Register(service.OnException)
            self.token.SendClientResponse = self.SendClientResponse
            self.token.SendServerRequest = self.SendServerRequest
            if rl[0].strip() == "POST":
                self.token.OnSuccessConnect()
                request = service.config.clientRequestModelDeserialize(body_raw.decode(service.config.encode))
                if request is None:
                    self.SendHttpError(code=ErrorCode.Common, message="RPC请求体格式错误", request=request)
                    return
                try:
                    result = service.ClientRequestReceiveProcess(self, request)
                    self.SendHttp(result)
                except Exception as e:
                    self.SendHttpError(code=ErrorCode.Common, message="异常:\n".join(e.args), request=request)
            else:
                WebSocketServerProtocol.processHandshake(self)

    def onOpen(self):
        if self.token is not None:
            self.token.OnSuccessConnect()

    def onMessage(self, payload, isBinary):
        if isBinary:
            self.SendErrorResponse(code=ErrorCode.Common, message="检测到二进制类型，暂不兼容")
            return
        else:
            request = self.token.service.config.clientRequestModelDeserialize(payload.decode(self.token.service.config.encode))
            if request is None:
                self.SendErrorResponse(request=request, code=ErrorCode.Common, message="RPC请求体格式错误")
                return
            try:
                result = self.token.service.ClientRequestReceiveProcess(self, request)
                self.SendClientResponse(result)
            except Exception as e:
                self.SendErrorResponse(request=request, code=ErrorCode.Common, message=e)

    def onClose(self, wasClean, code, reason):
        if self.token is not None:
            self.token.OnDisConnect()

    def SendErrorResponse(self, code=None, data=None, message=None, service_name=None, request_id=None, request=None):
        error = Error()
        error.Code = code
        error.Data = data
        error.Message = message
        if request is not None:
            request_id = request.Id
        response = ClientResponseModel(result=None,id=request_id,error=error)
        self.SendClientResponse(response)

    def SendClientResponse(self, response: ClientResponseModel):
        if response is None:
            return
        serialize = self.token.service.config.clientResponseModelSerialize
        responseBody = serialize(response)
        self.sendMessage(responseBody.encode(self.token.service.config.encode))

    def SendServerRequest(self, request: ServerRequestModel):
        """
        Send HTML page HTTP response.
        """
        if request is None:
            return
        self.OnLog(code=LogCode.Runtime, message=request)
        responseBody: str = self.token.service.config.serverRequestModelSerialize(request)
        self.sendMessage(responseBody.encode(self.token.service.config.encode))

    def SendHttpError(self, code=None,data=None,message=None,request:ClientRequestModel=None,error=None):
        response = ClientResponseModel()
        if error is None:
            error = Error()
        if request is not None:
            response.Id = request.Id
        if code is not None:
            error.COde = code
        if data is not None:
            error.Data = data
        if message is not None:
            error.Message = message
        self.SendHttp(response)

    def SendHttp(self, response_model):
        if response_model is None:
            return
        if self.token is not None:
            serialize = self.token.service.config.clientResponseModelSerialize
            encode = self.token.service.config.encode
        else:
            serialize = ServiceConfig.clientResponseModelSerializeFunc
            encode = "utf-8"
        response_json = serialize(response_model)
        response = "HTTP/1.1 200 OK\x0d\x0a"
        if self.factory.server is not None and self.factory.server != "":
            response += "Server : %s\x0d\x0a" % self.factory.server
        response += "Content-Type : application/json; charset=UTF-8\x0d\x0a"
        response += "\x0d\x0a\x0d\x0a"
        response += response_json
        a = response.encode(encode)
        self.sendData(a)
        self.dropConnection(abort=False)
