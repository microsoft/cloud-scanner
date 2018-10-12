from cloud_scanner.config.process_config import ProcessConfig
from .storage_container import StorageContainer


def register_storage_container(service_name, service_factory):
    def decorator(cls):
        StorageContainerFactory.register_factory(
            service_name,
            service_factory)

        return cls
    return decorator


class StorageContainerFactory:
    _factories = {}

    @classmethod
    def create(cls) -> StorageContainer:
        service_type = ProcessConfig().storage_container_type
        return cls._factories[service_type]()

    @classmethod
    def register_factory(cls, service_type: str, factory_func):
        cls._factories[service_type] = factory_func
