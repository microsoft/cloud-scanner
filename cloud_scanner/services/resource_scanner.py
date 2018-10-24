import json
import logging

from cloud_scanner.helpers import batch_list
from cloud_scanner.config.process_config import ProcessConfig
from cloud_scanner.contracts import (
    Queue, ResourceServiceFactory, QueueFactory, ResourceService
)


def _read_as_json(msg):
    """Decode message (UTF-8) and read into dictionary.

    :param msg: str to decode and deserialize
    :return: Dictionary from message
    """
    msg_body = msg.get_body().decode("utf-8")
    return json.loads(msg_body)


class ResourceScanner:
    """Scan cloud service for resources."""

    @staticmethod
    def process_queue_message(message):
        """Receives message from queue, which tells it which resources to scan
        from cloud provider.

        :param message: Task of which resources to scan
        :return: List of resources scanned from cloud provider
        """
        task = _read_as_json(message)

        queue_name = ProcessConfig().payload_queue_name

        resource_service = ResourceServiceFactory.create(
            task["providerType"], task["subscriptionId"])
        output_queue = QueueFactory.create(queue_name)

        task_processor = ResourceTaskProcessor(resource_service, output_queue)
        return task_processor.execute(task)


class ResourceTaskProcessor:
    """Process resource scanning tasks and return as dictionaries."""

    def __init__(self, resource_service: ResourceService, output_queue: Queue):
        self._resource_service = resource_service
        self._queue = output_queue

    def execute(self, task):
        """Execute scanning of resources.

        :param task: Defines which resources to scan
        :return: List of resources as dictionaries
        """
        subscription_id = task["subscriptionId"]
        if subscription_id is None:
            raise Exception(
                "Couldn't find a subscriptionId for the "
                "task: " + json.dumps(task))

        resource_type = task.get("typeName", None)
        logging.info(
            f"Received task for subscription {subscription_id}"
            f" and resource type {resource_type}")

        resource_filter = self._resource_service.get_filter(resource_type)
        resources = self._resource_service.get_resources(resource_filter)

        resource_count = 0

        # Transform resources to resource dictionaries
        resources = [resource.to_dict() for resource in resources]

        for batch in batch_list(resources,
                                batch_size=ProcessConfig().batch_size):
            self._queue.push(json.dumps(batch))
            resource_count += 1

        return resource_count
