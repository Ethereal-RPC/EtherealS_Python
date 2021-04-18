class ClientResponseModel:

    def __init__(self):
        self.JsonRpc: str = None
        self.Result: str = None
        self.Error: str = None
        self.Id: str = None
        self.Service: str = None
        self.ResultType: str = None

    def init(self, json_rpc, result, result_type, request_id, service, error):
        self.JsonRpc = json_rpc
        self.Result = result
        self.Error = error
        self.Id = request_id
        self.Service = service
        self.ResultType = result_type
