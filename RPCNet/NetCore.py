import json

from Model.BaseUserToken import BaseUserToken
from Model.ClientRequestModel import ClientRequestModel
from Model.ClientResponseModel import ClientResponseModel
from Model.RPCException import RPCException, ErrorCode
from Model.RPCType import RPCType
from RPCNet.Net import Net
from RPCNet.NetConfig import NetConfig
from RPCService import ServiceCore
from RPCService.Service import Service

nets = dict()


def Get(key: (str, str)) -> Net:
    return nets.get(key, None)


def RegisterByConfig(ip: str, port: str, config: NetConfig):
    key = (ip, port)
    if nets.get(key, None) is None:
        net = Net()
        net.config = config
        nets[key] = net
    else:
        raise RPCException(ErrorCode.RegisterError, "{0}已注册，无法重复注册！".format(key))
    return nets[key]

