from RPCService.Service import Service
from RPCService.ServiceConfig import ServiceConfig

__service = dict()


def Get(key):
    return __service.get(key, None)


def Get(service_name, hostname, port):
    return __service.get((service_name, hostname, port), None)


def Register(instance, service_name, ip, port, rpc_type):
    return Register(instance, service_name, ip, port, ServiceConfig(rpc_type))


def Register(instance, service_name, ip, port, config):
    key = (service_name, ip, port)
    if __service.get(key, None) is None:
        service = Service()
        service.register(instance, config)
        __service[key] = service
