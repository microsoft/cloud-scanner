from .resource_service import ResourceService


def register_resource_service(service_name, service_factory):
    def decorator(cls):
        ResourceServiceFactory.register_factory(
            service_name,
            service_factory)

        return cls
    return decorator


class ResourceServiceFactory:
    _factories = {}

    @classmethod
    def create(cls, service_type: str, subscription_id) -> ResourceService:
        return cls._factories[service_type](subscription_id)

    @classmethod
    def register_factory(cls, service_type: str, factory_func):
        cls._factories[service_type] = factory_func
