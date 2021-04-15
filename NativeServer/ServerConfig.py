class ServerConfig:
    num_connections = 1024
    buffer_size = 1024
    num_channels = 5
    auto_manage_token = True
    create_method = None

    def __init__(self, create_method):
        self.create_method = create_method
