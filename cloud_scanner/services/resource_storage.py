import logging

from cloud_scanner.contracts.resource import Resource
from cloud_scanner.contracts.resource_storage_factory import ResourceStorageFactory


class ResourceStorage:
    @staticmethod
    def process_queue_message(message):
        resource_storage = ResourceStorageFactory.create()
        resources = _parse_resources(message)

        resource_storage.write_entries(resources)
        return len(resources)


def _parse_resources(message):
    resource_list = message.get_json()

    # Convert message into a list if it isn"t already
    if not isinstance(resource_list, list):
        resource_list = [resource_list]

    logging.info(f"Found {len(resource_list)} resources to process")

    resource_list = [Resource(resource) for resource in resource_list]

    return resource_list
