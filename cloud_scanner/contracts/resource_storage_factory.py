from cloud_scanner.config.process_config import ProcessConfig
from .table_storage import TableStorage


def register_resource_storage(service_name, service_factory):
    """Register resource storage service.

    :param service_name: Name of service
    :param service_factory: Function to instantiate service
    :return: None
    """
    def decorator(cls):
        ResourceStorageFactory.register_factory(
            service_name,
            service_factory)

        return cls
    return decorator


class ResourceStorageFactory:
    """Instantiate resource storage services."""
    _factories = {}

    @classmethod
    def create(cls) -> TableStorage:
        """Create resource storage service.

        :return: Resource storage service object
        """
        service_type = ProcessConfig().resource_storage_type
        try:
            return cls._factories[service_type]()
        except KeyError:
            raise KeyError(
                f"Service type {service_type} is not "
                "registered for Resource Storage Service")

    @classmethod
    def register_factory(cls, service_type: str, factory_func):
        """Register factory.

        :param service_type: type of service of factory
        :param factory_func: Function to intantiate service
        :return: None
        """
        cls._factories[service_type] = factory_func
