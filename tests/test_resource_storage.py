import os

from cloud_scanner.services.resource_storage import ResourceStorage
from .unittest_base import TestCase, FakeQueueMessage


class ResourceStorageTest(TestCase):
    def test_process_queue_message_with_zero_resources(self):
        os.environ["PROVIDER_LIST"] = "simulator"

        json_data = '[]'
        message = FakeQueueMessage(bytes(json_data, 'utf-8'))
        resource_written = ResourceStorage.process_queue_message(message)

        self.assertEqual(0, resource_written)

    def test_process_queue_message_with_single_resource(self):
        os.environ["PROVIDER_LIST"] = "simulator"

        json_data = '''
            [{
                "id": "00000000-0000-0000-0000-000000000123",
                "accountId": "00000000-0000-0000-0000-000000000001",
                "providerType": "simulator",
                "type": "vm",
                "name": "MyResource",
                "group": "MyGroup",
                "location": "WestUS"
            }]
        '''

        message = FakeQueueMessage(bytes(json_data, 'utf-8'))
        resource_written = ResourceStorage.process_queue_message(message)

        self.assertEqual(1, resource_written)

    def test_process_queue_message_with_multiple_resources(self):
        os.environ["PROVIDER_LIST"] = "simulator"

        json_data = '''
            [{
                "id": "00000000-0000-0000-0000-000000000123",
                "accountId": "00000000-0000-0000-0000-000000000001",
                "providerType": "simulator",
                "type": "vm",
                "name": "MyResource",
                "group": "MyGroup",
                "location": "WestUS"
            },
            {
                "id": "00000000-0000-0000-0000-000000000124",
                "accountId": "00000000-0000-0000-0000-000000000002",
                "providerType": "simulator",
                "type": "vm",
                "name": "MyResource2",
                "group": "MyGroup2",
                "location": "EastUS"
            }]
        '''
        message = FakeQueueMessage(bytes(json_data, 'utf-8'))
        resource_written = ResourceStorage.process_queue_message(message)

        self.assertEqual(2, resource_written)
