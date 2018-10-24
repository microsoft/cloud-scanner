from cloud_scanner.config.process_config import ProcessConfig
from .storage_container import StorageContainer


def register_storage_container(service_name, service_factory):
    """Register storage container service.

    :param service_name: Name of service
    :param service_factory: Function to instantiate service
    :return: None
    """
    def decorator(cls):
        StorageContainerFactory.register_factory(
            service_name,
            service_factory)

        return cls
    return decorator


class StorageContainerFactory:
    """Instantiate storage container services."""
    _factories = {}

    @classmethod
    def create(cls) -> StorageContainer:
        """Create storage container service.

        :return: Storage container service object
        """
        service_type = ProcessConfig().storage_container_type
        try:
            return cls._factories[service_type]()
        except KeyError:
            raise KeyError(
                f"Service type {service_type} is not "
                f"registered for Storage Container Service")

    @classmethod
    def register_factory(cls, service_type: str, factory_func):
        """Register factory.

        :param service_type: type of service of factory
        :param factory_func: Function to intantiate service
        :return: None
        """
        cls._factories[service_type] = factory_func
