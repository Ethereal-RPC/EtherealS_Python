from Model.RPCTypeConfig import RPCTypeConfig


class RequestConfig:

    def __init__(self, config_type: RPCTypeConfig):
        self.types = config_type
        self.tokenEnable: bool = True
