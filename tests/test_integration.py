import logging
import json
import pytest
import unittest

from .unittest_base import FakeQueueMessage
from cloud_scanner.services.resource_scanner import ResourceScanner
from cloud_scanner.services.task_scheduler import TaskScheduler
from cloud_scanner.services.resource_storage import ResourceStorage
from cloud_scanner.contracts import ResourceStorageFactory, QueueFactory

from unittest import mock

from cloud_scanner.simulators import QueueSimulator

@pytest.mark.skip(reason="Integration test")
class IntegrationTest(unittest.TestCase):

    # Used when explicitly testing a task
    _test_subscription = '12341234-0000-0000-0000-123412341234'

    # 
    _write_to_storage = True

    def schedule_tasks(self):
        result_messages = []

        def push_intercept(msg):
            queue_msg = FakeQueueMessage(bytes(msg, 'utf-8'))
            result_messages.append(queue_msg)
        
        with mock.patch.object(QueueSimulator, "push", side_effect=push_intercept):
            logging.info("Running Task Scheduler")
            TaskScheduler.execute()
        
        # Will fail if no tasks were configured
        assert(result_messages)

        test_msg = result_messages[0].get_json()
        logging.info(f"Inspecting first message: {test_msg}")
        assert(test_msg['providerType'])
        assert(test_msg['subscriptionId'])
        assert(test_msg['typeName'])
        
        return result_messages
    
    @staticmethod
    def _create_dummy_task(sub_id, resource_type, provider='azure'):
        dummy_task = {
            'providerType': provider,
            'subscriptionId': sub_id,
            'typeName': resource_type
        }
        task_string = json.dumps(dummy_task)
        msg = FakeQueueMessage(bytes(task_string, 'utf-8'))
        return msg

    def scan_resource_test(self, task_msg):
        result_messages = []

        def push_intercept(msg):
            queue_msg = FakeQueueMessage(bytes(msg, 'utf-8'))
            result_messages.append(queue_msg)
        
        with mock.patch.object(QueueFactory, "create") as cm:
            fake_push = mock.MagicMock(side_effect=push_intercept)
            fake_queue = mock.MagicMock(push=fake_push)
            cm.return_value = fake_queue

            logging.info(f"Running Resource Scanner")
            ResourceScanner.process_queue_message(task_msg)
        
        # Will fail if no resources were found
        assert(result_messages)

        test_msg = result_messages[0].get_json()
        logging.info(f"Inspecting first message: {test_msg}")
        assert(test_msg["id"])
        assert(test_msg["name"])
        assert(test_msg["type"])
        assert(test_msg["location"])
        
        return result_messages
    
    def store_resource_test(self, resource_msg):
        if self._write_to_storage:
            ResourceStorage.process_queue_message(resource_msg)
            return
        
        written_resources = []
        def write_intercept(resource):
            logging.info(f"Intercepted storage write {resource.to_normalized_dict()}")
            written_resources.append(resource)

        with mock.patch.object(ResourceStorageFactory, "create") as cm:
            fake_write = mock.MagicMock(side_effect=write_intercept)
            fake_storage = mock.MagicMock(write=fake_write)
            cm.return_value = fake_storage

            logging.info(f"Running Resource Storage")
            ResourceStorage.process_queue_message(resource_msg)
        
        assert(written_resources)
        normalized_resource = written_resources[0].to_normalized_dict()

        assert(normalized_resource["ARN"])
        assert(normalized_resource["ResourceId"])
        assert(normalized_resource["ResourceType"])
        assert(normalized_resource["Region"])
    
    def _run_task(self, task):
        resources = self.scan_resource_test(task)

        for resource_msg in resources:
            self.store_resource_test(resource_msg)

    # Full integration test of everything defined by configuration
    def test_integration(self):
        tasks = self.schedule_tasks()

        for task in tasks:
            self._run_task(task)
    
    # Only test storage accounts
    def test_storage_account(self):
        storage_task = self._create_dummy_task(self._test_subscription, 'Microsoft.Storage/storageAccounts')
        self._run_task(storage_task)
    
    # Only test virtual Machines
    def test_virtual_machines(self):
        storage_task = self._create_dummy_task(self._test_subscription, 'Microsoft.Compute/virtualMachines')
        
        self._run_task(storage_task)
