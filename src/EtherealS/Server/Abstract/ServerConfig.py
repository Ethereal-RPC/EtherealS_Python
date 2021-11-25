import json
from abc import ABC

from EtherealS.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealS.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealS.Core.Model import ServerRequestModel
from EtherealS.Utils.JsonTool import JSONClientResponseModel


class ServerConfig(ABC):

    def __init__(self):
        self.encode = "utf-8"