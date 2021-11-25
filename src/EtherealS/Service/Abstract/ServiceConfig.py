import json
from abc import ABC

from EtherealS.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealS.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealS.Core.Model.ServerRequestModel import ServerRequestModel
from EtherealS.Service.Abstract import Service
from EtherealS.Utils.JsonTool import JSONClientResponseModel


def clientResponseModelSerializeFunc(obj: ClientResponseModel) -> str:
    return json.dumps(obj.__dict__, cls=JSONClientResponseModel, ensure_ascii=False)


def clientRequestModelDeserializeFunc(_json: str) -> ClientRequestModel:
    instance = ClientRequestModel()
    di = json.loads(_json)
    try:
        instance.__dict__ = di
    except:
        instance = None
    return instance


def serverRequestModelSerializeFunc(obj: ServerRequestModel) -> str:
    return json.dumps(obj.__dict__, ensure_ascii=False)


class ServiceConfig(ABC):

    def __init__(self):
        self.authoritable = False
        self.auto_manage_token = True
        self.encode = "utf-8"
        self.serverRequestModelSerialize = serverRequestModelSerializeFunc
        self.clientRequestModelDeserialize = clientRequestModelDeserializeFunc
        self.clientResponseModelSerialize = clientResponseModelSerializeFunc
