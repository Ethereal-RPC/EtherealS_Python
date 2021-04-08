class ClientResponseModel:
    JsonRpc = None
    Result = None
    Error = None
    Id = None
    Service = None
    ResultType = None

    def __init__(self, json_rpc, result, result_type, request_id, service, error) -> None:
        super().__init__()
        self.JsonRpc = json_rpc
        self.Result = result
        self.Error = error
        self.Id = request_id
        self.Service = service
        self.ResultType = result_type
