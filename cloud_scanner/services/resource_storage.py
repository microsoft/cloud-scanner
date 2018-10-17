import logging

from cloud_scanner.contracts import Resource, ResourceStorageFactory


class ResourceStorage:
    """Store resources from scanning."""
    @staticmethod
    def process_queue_message(message):
        """Receives resources from queue and stores in registered service.

        :param message: Payload of resources to store
        :return: Number of resources stored in service
        """
        resource_storage = ResourceStorageFactory.create()
        resources = _parse_resources(message)

        resource_storage.write_entries(resources)
        return len(resources)


def _parse_resources(message):
    """Parse message from queue as JSON of resources.

    :param message: JSON of resources
    :return: Deserialized list of Resource objects
    """
    resource_list = message.get_json()

    # Convert message into a list if it isn"t already
    if not isinstance(resource_list, list):
        resource_list = [resource_list]

    logging.info(f"Found {len(resource_list)} resources to process")

    resource_list = [Resource(resource) for resource in resource_list]

    return resource_list
