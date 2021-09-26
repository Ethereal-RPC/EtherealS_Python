from autobahn.twisted import WebSocketServerProtocol
from autobahn.websocket import protocol

from Core.Model import ClientRequestModel
from Core.Model.ClientResponseModel import ClientResponseModel
from Core.Model.Error import Error, ErrorCode
from Core.Model.TrackException import TrackException
from Core.Model.TrackLog import TrackLog, LogCode
from Core.Model import ServerRequestModel
from Net import NetCore
from Net.Abstract.Net import Net
from Core.Event import Event
from Server.Abstract.BaseToken import BaseToken


class WebSocketBaseToken(BaseToken, WebSocketServerProtocol):
    def serialize(self):
        return None

    def __init__(self):
        super(BaseToken, self).__init__()
        super(WebSocketServerProtocol, self).__init__()
        self.prefixes = None

    def processHandshake(self):
        # only proceed when we have fully received the HTTP request line and all headers
        #
        end_of_header = self.data.find(b"\x0d\x0a\x0d\x0a")
        if end_of_header >= 0:

            http_request_data = self.data[:end_of_header + 4]
            body = self.data[end_of_header + 4:].decode(self.config.encode)

            # extract HTTP status line and headers
            #
            try:
                http_status_line, http_headers, http_headers_cnt = \
                    protocol.parseHttpHeader(http_request_data)
            except Exception as e:
                return self.failHandshake("Error during parsing of HTTP status line / request headers : {0}".format(e))

            # HTTP Request line : METHOD, VERSION
            #
            rl = http_status_line.split()
            if rl[0].strip() == "POST":
                self.__OnConnect()
                request = self.config.clientRequestModelDeserialize(body)
                net = NetCore.Get(self.net_name)
                if request is None:
                    self.__SendHttpError(request=request, code=ErrorCode.Common, message="RPC请求体格式错误")
                    return
                if net is None:
                    self.__SendHttpError(request=request, code=ErrorCode.Common,
                                         message="{0}找不到Net".format(self.net_name))
                    return
                try:
                    result = net.ClientRequestReceiveProcess(self, request)
                    self.__SendHttp(result)
                except Exception as e:
                    self.__SendHttpError(request=request, code=ErrorCode.Common, message=e.args)
                self.dropConnection(abort=False)
            else:
                WebSocketServerProtocol.processHandshake(self)

    def onConnect(self, request):
        pass

    def onOpen(self):
        self.__OnConnect()

    def onMessage(self, payload, isBinary):
        if isBinary:
            self.SendErrorResponse(code=ErrorCode.Common, message="检测到二进制类型，暂不兼容")
            return
        else:
            request = self.config.clientRequestModelDeserialize(payload.decode(self.config.encode))
            if request is None:
                self.SendErrorResponse(request=request, code=ErrorCode.Common, message="RPC请求体格式错误")
                return
            net = NetCore.Get(self.net_name)
            if net is None:
                self.SendErrorResponse(request=request, code=ErrorCode.Common,
                                       message="{0}找不到Net".format(self.net_name))
            try:
                result = net.ClientRequestReceiveProcess(self, request)
                self.SendClientResponse(result)
            except Exception as e:
                self.SendErrorResponse(request=request, code=ErrorCode.Common, message=e)

    def onClose(self, wasClean, code, reason):
        self.__OnDisConnect()

    def __OnConnect(self):
        self.connect_event.OnEvent()

    def __OnDisConnect(self):
        self.disconnect_event.OnEvent()

    def SendErrorResponse(self, code=None, data=None, message=None, service_name=None, request_id=None, request=None):
        error = Error()
        error.Code = code
        error.Data = data
        error.Message = message
        if request is not None:
            request_id = request.Id
            service_name = request.Service
        response = ClientResponseModel(result=None, result_type=None, request_id=request_id,
                                       service=service_name, error=error)
        self.SendClientResponse(response)

    def SendClientResponse(self, response: ClientResponseModel):
        responseBody = self.config.clientResponseModelSerialize(response)
        self.sendMessage(responseBody.encode(self.config.encode))

    def SendServerRequest(self, request: ServerRequestModel):
        """
        Send HTML page HTTP response.
        """
        self.OnLog(code=LogCode.Runtime, message=request)
        responseBody: str = self.config.serverRequestModelSerialize(request)
        self.sendMessage(responseBody.encode(self.config.encode))

    def __SendHttpError(self, **kwargs):
        error = Error()
        error.Code = kwargs.get("code")
        error.Data = kwargs.get("data")
        error.Message = kwargs.get("message")
        request: ClientRequestModel = kwargs.get("request")
        service = None
        request_id = None
        if request is not None:
            request_id = request.Id
            service = request.Service
        response = ClientResponseModel(result=None, result_type=None, request_id=request_id,
                                       service=service, error=error)
        self.__SendHttp(response)

    def __SendHttp(self, response_model):
        response_json = self.config.clientResponseModelSerialize(response_model)
        response = "HTTP/1.1 200 OK\x0d\x0a"
        if self.factory.server is not None and self.factory.server != "":
            response += "Server : %s\x0d\x0a" % self.factory.server
        response += "Content-Type : application/json; charset=UTF-8\x0d\x0a"
        response += "\x0d\x0a\x0d\x0a"
        response += response_json
        a = response.encode("utf8")
        self.sendData(a)

