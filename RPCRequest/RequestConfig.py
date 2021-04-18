from Model.RPCType import RPCType


class RequestConfig:

    def __init__(self, config_type: RPCType):
        self.type = config_type
        self.tokenEnable: bool = True
