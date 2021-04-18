class ServerConfig:

    def __init__(self, create_method):
        self.create_method = create_method
        self.num_connections = 1024
        self.buffer_size = 1024
        self.num_channels = 5
        self.auto_manage_token = True
        self.encode = "utf-8"
