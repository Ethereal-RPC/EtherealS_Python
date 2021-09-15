import json

from Model.ClientRequestModel import ClientRequestModel
from Model.ClientResponseModel import ClientResponseModel
from Model.ServerRequestModel import ServerRequestModel
from Utils.JsonTool import JSONClientResponseModel


class ServerConfig:

    def __init__(self, create_method):
        self.create_method = create_method
        self.num_connections = 1024
        self.buffer_size = 1024
        self.num_channels = 5
        self.auto_manage_token = True
        self.encode = "utf-8"

        def serverRequestModelSerializeFunc(obj: ServerRequestModel) -> str:
            return json.dumps(obj.__dict__, ensure_ascii=False)

        self.serverRequestModelSerialize = serverRequestModelSerializeFunc

        def clientRequestModelDeserializeFunc(_json: str) -> ClientRequestModel:
            instance = ClientRequestModel()
            di = json.loads(_json)
            try:
                instance.__dict__ = di
            except:
                instance = None
            return instance

        self.clientRequestModelDeserialize = clientRequestModelDeserializeFunc

        def clientResponseModelSerializeFunc(obj: ClientResponseModel) -> str:
            return json.dumps(obj.__dict__, cls=JSONClientResponseModel, ensure_ascii=False)

        self.clientResponseModelSerialize = clientResponseModelSerializeFunc
