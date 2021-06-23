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


def Get(name):
    return nets.get(name)


def Register(**kwargs):
    name = kwargs.get("name")
    config: NetConfig = kwargs.get("config")
    if nets.get(name, None) is None:
        net = Net()
        net.name = name
        net.config = config
        nets[name] = net
    else:
        raise RPCException(ErrorCode.Core, "{0}已注册，无法重复注册！".format(name))
    return nets[name]

