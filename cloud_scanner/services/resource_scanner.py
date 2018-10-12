import json
import logging

from cloud_scanner.helpers import batch_list
from cloud_scanner.config.process_config import ProcessConfig
from cloud_scanner.contracts import Queue
from cloud_scanner.contracts.resource_service_factory import ResourceServiceFactory
from cloud_scanner.contracts.queue_factory import QueueFactory
from cloud_scanner.contracts.resource_service import ResourceService


def _read_as_json(msg):
    msg_body = msg.get_body().decode("utf-8")
    return json.loads(msg_body)


class ResourceScanner:

    @staticmethod
    def process_queue_message(message):
        task = _read_as_json(message)

        queue_name = ProcessConfig().payload_queue_name

        resource_service = ResourceServiceFactory.create(task["providerType"], task["subscriptionId"])
        output_queue = QueueFactory.create(queue_name)

        task_processor = ResourceTaskProcessor(resource_service, output_queue)
        return task_processor.execute(task)


class ResourceTaskProcessor:
    def __init__(self, resource_service: ResourceService, output_queue: Queue):
        self._resource_service = resource_service
        self._queue = output_queue

    def execute(self, task):
        subscription_id = task["subscriptionId"]
        if subscription_id is None:
            raise Exception("Couldn't find a subscriptionId for the task: " + json.dumps(task))

        resource_type = task.get("typeName", None)
        logging.info(f"Received task for subscription {subscription_id} and resource type {resource_type}")

        resource_filter = self._resource_service.get_filter(resource_type)
        resources = self._resource_service.get_resources(resource_filter)

        resource_count = 0

        # Transform resources to resource dictionaries
        resources = [resource.to_dict() for resource in resources]

        for batch in batch_list(resources, batch_size=ProcessConfig().batch_size):
            self._queue.push(json.dumps(batch))
            resource_count += 1

        return resource_count
