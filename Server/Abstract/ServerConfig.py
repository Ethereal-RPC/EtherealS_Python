import json
from abc import ABC

from Core.Model.ClientRequestModel import ClientRequestModel
from Core.Model.ClientResponseModel import ClientResponseModel
from Core.Model import ServerRequestModel
from Utils.JsonTool import JSONClientResponseModel


class ServerConfig(ABC):

    def __init__(self, create_method):
        self.create_method = create_method
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
