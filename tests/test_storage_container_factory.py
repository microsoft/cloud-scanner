import os

from cloud_scanner.contracts.storage_container_factory import StorageContainerFactory, register_storage_container
from .unittest_base import TestCase
from unittest.mock import patch

def create_func():
    return StorageContainerMock()


@register_storage_container('test', create_func)
class StorageContainerMock:
    pass


class TestStorageContainerFactory(TestCase):
    def setUp(self):
        os.environ["CONFIG_CONTAINER"] = "test-container"

    def test_create_container_simulator(self):
        os.environ["STORAGE_CONTAINER_TYPE"] = "simulator"

        container = StorageContainerFactory.create()
        self.assertIsNotNone(container)
        self.assertEqual(type(container).__name__, "MockBlobStorageSimulator")

    @patch.object(StorageContainerFactory, 'register_factory')
    def test_register_storage_container_decorator(self, mock_register_factory):
        os.environ["STORAGE_CONTAINER_TYPE"] = "test"
        
        decorator = register_storage_container('test', create_func)
        decorator(StorageContainerFactory)

        mock_register_factory.assert_called_once_with('test', create_func)

        container = StorageContainerFactory.create()
        self.assertIsNotNone(container)
        self.assertEqual(type(container).__name__, "StorageContainerMock")

    def test_unknown_provider(self):
        os.environ["STORAGE_CONTAINER_TYPE"] = "unknown"
        test_error = None

        try:
            StorageContainerFactory.create()
        except Exception as create_error:
            test_error = create_error

        self.assertFalse(test_error is None, "Expected error to be thrown for invalid provider")


        



