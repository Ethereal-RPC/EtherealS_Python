from RPCNet import NetCore


class BaseUserToken:
    serverKey = None
    net = None
    key = None
    connect_event = list()
    disconnect_event = list()

    def register(self, replace=False):
        tokens = NetCore.GetTokens(self.serverKey)
        if tokens is not None:
            if replace is False:
                if tokens.get(self.key,None) is not None:
                    return True
            tokens[self.key] = self
            return True

    def unRegister(self):
        tokens = NetCore.GetTokens(self.serverKey)
        if tokens.get(self.key, None) is not None:
            del tokens[self.key]
        return True

    def getTokens(self):
        return NetCore.GetTokens(self.serverKey)

    def getToken(self, key):
        tokens = NetCore.GetTokens(self.serverKey)
        return tokens.get(key, None)

    def OnConnect(self):
        for method in self.connect_event:
            method.__call__(self)

    def DisConnect(self):
        for method in self.disconnect_event:
            method.__call__(self)
