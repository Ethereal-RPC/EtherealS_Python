import threading


class ClientRequestModel:

    def __init__(self):
        self.Result = None
        self.JsonRpc = None
        self.MethodId = None
        self.Params: list = None
        self.Id = None
        self.Service = None
        self.Sign = threading.Event()

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
