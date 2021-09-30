import json

from EtherealS.Core.Model import ClientRequestModel
from EtherealS.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealS.Core.Model import ServerRequestModel
from EtherealS.Server.Abstract.ServerConfig import ServerConfig
from EtherealS.Utils.JsonTool import JSONClientResponseModel


class WebSocketServerConfig(ServerConfig):

    def __init__(self):
        super().__init__()
