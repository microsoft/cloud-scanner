from cloud_scanner.config.process_config import ProcessConfig
from .table_storage import TableStorage


def register_resource_storage(service_name, service_factory):
    def decorator(cls):
        ResourceStorageFactory.register_factory(
            service_name,
            service_factory)

        return cls
    return decorator


class ResourceStorageFactory:
    _factories = {}

    @classmethod
    def create(cls) -> TableStorage:
        service_type = ProcessConfig().resource_storage_type
        return cls._factories[service_type]()

    @classmethod
    def register_factory(cls, service_type: str, factory_func):
        cls._factories[service_type] = factory_func
