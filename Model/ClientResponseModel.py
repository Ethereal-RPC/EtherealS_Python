class ClientResponseModel:
    JsonRpc: str = None
    Result: str = None
    Error: str = None
    Id: str = None
    Service: str = None
    ResultType: str = None

    def init(self, json_rpc, result, result_type, request_id, service, error):
        self.JsonRpc = json_rpc
        self.Result = result
        self.Error = error
        self.Id = request_id
        self.Service = service
        self.ResultType = result_type
