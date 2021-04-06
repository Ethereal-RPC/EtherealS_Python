from Model.RPCType import RPCType


class ServiceConfig:
    interceptorEvent = list()
    tokenEnable = None
    type: RPCType = None
    authoritable = None

    def __init__(self, type):
        self.type = type
