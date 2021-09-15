class ClientRequestModel:

    def __init__(self, **kwargs):
        self.Type = "ER-1.0-ClientRequest"
        self.JsonRpc = None
        self.MethodId: str
        self.Params: list
        self.Id = None
        self.Service = None
