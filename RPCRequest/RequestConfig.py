from Model.RPCException import RPCException
from Model.RPCLog import RPCLog
from Model.RPCTypeConfig import RPCTypeConfig
from Utils.Event import Event


class RequestConfig:

    def __init__(self, config_type: RPCTypeConfig):
        self.types = config_type
        self.tokenEnable: bool = True


