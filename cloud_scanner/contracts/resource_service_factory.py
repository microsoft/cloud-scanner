from .resource_service import ResourceService


def register_resource_service(service_name, service_factory):
    """Register resource service.

    :param service_name: Name of service
    :param service_factory: Function to instantiate service
    :return: None
    """
    def decorator(cls):
        ResourceServiceFactory.register_factory(
            service_name,
            service_factory)

        return cls
    return decorator


class ResourceServiceFactory:
    """Instantiate resource services."""
    _factories = {}

    @classmethod
    def create(cls, service_type: str, subscription_id) -> ResourceService:
        """Create resource service.

        :param service_type: type of service
        :param subscription_id: cloud service subscription or account ID
        :return: Resource service object
        """
        try:
            return cls._factories[service_type](subscription_id)
        except KeyError:
            raise KeyError(
                f"Service type {service_type} is not "
                "registered for Resource Service")

    @classmethod
    def register_factory(cls, service_type: str, factory_func):
        """Register factory.

        :param service_type: type of service of factory
        :param factory_func: Function to intantiate service
        :return: None
        """
        cls._factories[service_type] = factory_func
