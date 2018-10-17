import os

from cloud_scanner.contracts import ResourceServiceFactory, register_resource_service, ResourceService
from .unittest_base import TestCase
from unittest.mock import patch


def create_func(subscription_id):
    return ResourceServiceMock()


@register_resource_service('test', create_func)
class ResourceServiceMock():
    pass


class TestResourceServiceFactory(TestCase):
    def test_simulator_provider(self):
        service = ResourceServiceFactory.create("simulator", "00000000-0000-0000-0000-000000000000")
        self.assertFalse(service is None)
        self.assertEqual("ResourceServiceSimulator", type(service).__name__)

    @patch.object(ResourceServiceFactory, 'register_factory')
    def test_register_resource_service_decorator(self, mock_register_factory):
        decorator = register_resource_service('test', create_func)
        decorator(ResourceServiceFactory)

        mock_register_factory.assert_called_once_with('test', create_func)

        resource_service = ResourceServiceFactory.create("test", "00000000-0000-0000-0000-000000000000")
        self.assertIsNotNone(resource_service)
        self.assertEqual(type(resource_service).__name__, "ResourceServiceMock")

    def test_unknown_provider(self):
        test_error = None

        try:
            ResourceServiceFactory.create("unknown", "00000000-0000-0000-0000-000000000000")
        except Exception as create_error:
            test_error = create_error

        self.assertFalse(test_error is None, "Expected error to be thrown for invalid provider")
