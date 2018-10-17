import os

from cloud_scanner.simulators import MockBlobStorageSimulator
from cloud_scanner.services.task_scheduler import TaskScheduler
from cloud_scanner.contracts import CloudConfigReader
from .unittest_base import TestCase


class TestScheduler(TestCase):
    def setUp(self):
        os.environ["STORAGE_CONTAINER_TYPE"] = "simulator"
        os.environ["QUEUE_TYPE"] = "simulator"
        os.environ["TASK_QUEUE_NAME"] = "test-queue"

    def read_config(self):
        container = MockBlobStorageSimulator()
        config_reader =  CloudConfigReader(container)
        return config_reader.read_config()

    def test_latest_config_is_picked(self):

        result = self.read_config()
        self.assertFalse(result is None)

        providers = result['providers']
        for provider in providers:
            self.assertFalse(provider is None)

    def test_tasks_are_created(self):

        result = self.read_config()
        tasks = TaskScheduler._create_tasks('simulator', result["providers"][0])
        for task in tasks:
            id = task['subscriptionId']
            type = task['typeName']
            self.assertFalse(id is None)
            self.assertFalse(type is None)

    def test_push_tasks_to_queue(self):
        # Get expected number of tasks for simulator provider
        result = self.read_config()
        tasks = TaskScheduler._create_tasks('simulator', result["providers"][0])

        task_count = TaskScheduler.execute()
        self.assertEqual(len(tasks), task_count)
