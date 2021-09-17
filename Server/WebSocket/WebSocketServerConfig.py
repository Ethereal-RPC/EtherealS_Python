import json

from Core.Model import ClientRequestModel
from Core.Model.ClientResponseModel import ClientResponseModel
from Core.Model import ServerRequestModel
from Server.Abstract.ServerConfig import ServerConfig
from Utils.JsonTool import JSONClientResponseModel


class WebSocketServerConfig(ServerConfig):

    def __init__(self, create_method):
        super().__init__(create_method)
