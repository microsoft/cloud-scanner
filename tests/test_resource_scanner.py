import json
import os

from cloud_scanner.simulators import ResourceServiceSimulator, QueueSimulator
from cloud_scanner.services.resource_scanner import ResourceScanner, ResourceTaskProcessor
from .unittest_base import TestCase, FakeQueueMessage
from cloud_scanner.config import ProcessConfig


class TestScanResources(TestCase):
    def setUp(self):
        os.environ["STORAGE_CONTAINER_TYPE"] = "simulator"
        os.environ["RESOURCE_STORAGE_TYPE"] = "simulator"
        os.environ["QUEUE_TYPE"] = "simulator"
        os.environ["PAYLOAD_QUEUE_NAME"] = "test-queue"

    def test_simulator_task(self):
        json_data = '''
            {
                "providerType": "simulator",
                "subscriptionId": "00000000-0000-0000-0000-000000000001",
                "typeName": "Microsoft.Compute/virtualMachines"
            }
        '''
        message = FakeQueueMessage(bytes(json_data, 'utf-8'))
        count = ResourceScanner.process_queue_message(message)

        self.assertEqual(count, 1)

    def test_task_processor(self):
        data = {
            "subscriptionId" : "12345678-0000-0000-0000-123412341234",
            "typeName" : "storage"
        }
        resource_service = ResourceServiceSimulator()
        queue = QueueSimulator("test_queue")

        # Get the expected resources from the provider
        resources = resource_service.get_resources(data["subscriptionId"])

        task_processor = ResourceTaskProcessor(resource_service, queue)
        task_processor.execute(data)

        item = queue.pop()

        self.assertEqual(len(json.loads(item)), len(resources))

    def test_batching(self):
        key = 'RESOURCE_BATCH_SIZE'
        if key in os.environ:
            del os.environ[key]
        process_config = ProcessConfig()
        self.assertEqual(16, process_config.batch_size)

        os.environ[key] = '100'
        self.assertEqual(100, process_config.batch_size)


