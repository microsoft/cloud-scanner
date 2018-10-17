import os

from cloud_scanner.contracts.resource_storage_factory import ResourceStorageFactory, register_resource_storage
from .unittest_base import TestCase
from unittest.mock import patch

def create_func():
    return ResourceStorageMock()


@register_resource_storage('test', create_func)
class ResourceStorageMock():
    pass
    

class TestResourceStorageFactory(TestCase):
    def test_simulator_resource_storage(self):
        os.environ["RESOURCE_STORAGE_TYPE"] = "simulator"

        resource_storage = ResourceStorageFactory.create()
        self.assertIsNotNone(resource_storage)
        self.assertEqual(type(resource_storage).__name__, "TableStorageSimulator")

    @patch.object(ResourceStorageFactory, 'register_factory')
    def test_register_resource_storage_decorator(self, mock_register_factory):
        os.environ["RESOURCE_STORAGE_TYPE"] = "test"
        
        decorator = register_resource_storage('test', create_func)
        decorator(ResourceStorageFactory)

        mock_register_factory.assert_called_once_with('test', create_func)

        resource_service = ResourceStorageFactory.create()
        self.assertIsNotNone(resource_service)
        self.assertEqual(type(resource_service).__name__, "ResourceStorageMock")

    def test_unknown_provider(self):
        os.environ["RESOURCE_STORAGE_TYPE"] = "unknown"
        test_error = None

        try:
            ResourceStorageFactory.create()
        except Exception as create_error:
            test_error = create_error

        self.assertFalse(test_error is None, "Expected error to be thrown for invalid provider")
