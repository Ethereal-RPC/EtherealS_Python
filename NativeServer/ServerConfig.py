import json

from Model.ClientRequestModel import ClientRequestModel
from Model.ClientResponseModel import ClientResponseModel
from Model.RPCException import RPCException
from Model.RPCLog import RPCLog
from Model.ServerRequestModel import ServerRequestModel
from Utils.Event import Event


class ServerConfig:

    def __init__(self, create_method):
        self.create_method = create_method
        self.num_connections = 1024
        self.buffer_size = 1024
        self.num_channels = 5
        self.auto_manage_token = True
        self.encode = "utf-8"
        self.exception_event = Event()
        self.log_event = Event()

        def serverRequestModelSerializeFunc(obj: ServerRequestModel) -> str:
            return json.dumps(obj)

        self.serverRequestModelSerialize = serverRequestModelSerializeFunc

        def clientRequestModelDeserializeFunc(_json: str) -> ClientRequestModel:
            instance = ClientRequestModel()
            di = json.loads(_json)
            try:
                instance.__dict__ = di
            except:
                instance = di
            return instance

        self.clientRequestModelDeserialize = clientRequestModelDeserializeFunc

        def clientResponseModelSerializeFunc(obj: ClientResponseModel) -> str:
            return json.dumps(obj)

        self.clientResponseModelSerialize = clientResponseModelSerializeFunc

    def OnLog(self, **kwargs):
        code = kwargs.get("code")
        message = kwargs.get("message")
        server = kwargs.get("server")
        log = kwargs.get("log")
        if log is None:
            log = RPCLog(code, message)
        self.log_event.onEvent(log=log, server=server)

    def OnException(self, **kwargs):
        code = kwargs.get("code")
        message = kwargs.get("message")
        exception = kwargs.get("exception")
        server = kwargs.get("server")
        if exception is None:
            exception = RPCException(code, message)
        self.exception_event.onEvent(exception=exception, server=server)
        raise exception
