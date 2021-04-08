from Model.RPCType import RPCType


class RequestConfig:
    tokenEnable: bool
    type: RPCType

    def __init__(self, config_type: RPCType):
        self.type = config_type
