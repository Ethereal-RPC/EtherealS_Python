import threading


class ClientRequestModel:
    result = None
    jsonRpc = None
    methodId = None
    params = None
    id = None
    service = None
    sign = threading.Event()

    def __init__(self, json_rpc, service, method_id, params):
        self.jsonRpc = json_rpc
        self.service = service
        self.methodId = method_id
        self.params = params

    def set(self, result):
        self.result = result
        self.sign.set()

    def get(self, timeout):
        while self.result is None:
            if timeout == -1:
                self.sign.wait()
            else:
                self.sign.wait(timeout)
        return self.result
