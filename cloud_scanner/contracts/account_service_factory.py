from .account_service import AccountService


def register_account_service(service_name, service_factory):
    """Registers an account service for a cloud provider.

    :param service_name: name of cloud provider ('aws' or 'azure')
    :param service_factory:
    :return:
    """
    def decorator(cls):
        AccountServiceFactory.register_factory(
            service_name,
            service_factory)

        return cls
    return decorator


class AccountServiceFactory:
    """Factory to instantiate account services for cloud providers."""
    _factories = {}

    @classmethod
    def create(cls, service_type: str) -> AccountService:
        """Create an account service based on service type.

        :param service_type: str
        :return:
        """
        try:
            return cls._factories[service_type]()
        except KeyError:
            raise KeyError(
                f"Service type {service_type} is "
                "not registered for Account Service")

    @classmethod
    def get_providers(cls):
        return [cls.create(key) for key in cls._factories]

    @classmethod
    def register_factory(cls, service_type: str, factory_func):
        cls._factories[service_type] = factory_func
