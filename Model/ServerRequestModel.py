class ServerRequestModel:

    def __init__(self, json_rpc, method_id, params, service) -> None:
        super().__init__()
        self.JsonRpc = json_rpc
        self.MethodId = method_id
        self.Params = params
        self.Service = service
