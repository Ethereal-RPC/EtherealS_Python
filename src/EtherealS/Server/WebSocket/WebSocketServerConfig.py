import json

from EtherealS.Core.Model import ClientRequestModel
from EtherealS.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealS.Core.Model import ServerRequestModel
from EtherealS.Server.Abstract.ServerConfig import ServerConfig
from EtherealS.Utils.JsonTool import JSONClientResponseModel


class WebSocketServerConfig(ServerConfig):

    def __init__(self, create_method):
        super().__init__(create_method)
