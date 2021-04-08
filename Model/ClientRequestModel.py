import threading


class ClientRequestModel:
    Result = None
    JsonRpc = None
    MethodId = None
    Params: list = None
    Id = None
    Service = None
    Sign = threading.Event()

    def __init__(self, json_rpc, service, method_id, params):
        super().__init__()
        self.JsonRpc = json_rpc
        self.Service = service
        self.MethodId = method_id
        self.Params = params

    def set(self, result):
        self.Result = result
        self.Sign.set()

    def get(self, timeout):
        while self.Result is None:
            if timeout == -1:
                self.Sign.wait()
            else:
                self.Sign.wait(timeout)
        return self.Result
