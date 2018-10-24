from cloud_scanner.config.process_config import ProcessConfig
from .queue import Queue


def register_queue_service(service_name, service_factory):
    """Decorator used to register an implementation of a queue with the queue
    factory.

    :param service_name: The name to register this type of queue as.
    :param service_factory: A function or lambda that takes a queue_name
        (as a string) and will return an instance of the queue implementation.
    """

    def decorator(cls):
        QueueFactory.register_factory(
            service_name,
            service_factory)
        return cls
    return decorator


class QueueFactory:
    """Singleton factory responsible for creating queues."""

    _factories = {}

    @classmethod
    def create(cls, queue_name: str) -> Queue:
        """Returns a queue with 'queue_name' of type specified in the config
        "QUEUE_TYPE" property.

        :param queue_name: Name of the queue
        :return: Implemented instance of the Queue contract
        """
        # @TODO: No way of using more than one type of queue
        # type since service_type is being read from config
        # instead of being passed in/dynamic.
        service_type = ProcessConfig().queue_type
        try:
            return cls._factories[service_type](queue_name)
        except KeyError:
            raise KeyError(
                f"Service type {service_type} is not "
                "registered for Queue Service")

    @classmethod
    def register_factory(cls, service_type: str, factory_func):
        """Utility function used to register a type of queue with a string
        name.

        Primarily used by the 'register_queue_service' decorator.
        """
        cls._factories[service_type] = factory_func
