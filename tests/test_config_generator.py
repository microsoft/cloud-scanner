import json

from cloud_scanner.simulators import MockBlobStorageSimulator
from cloud_scanner.contracts import CloudConfigGenerator
from .unittest_base import TestCase


class CloudConfigGeneratorTest(TestCase):

    types = ['vm', 'storage']
    provider_types = ['simulator']

    expected_config = {
        "providers": [{
            "type": "simulator",
            "subscriptions": [
                {
                    "subscriptionId": "00000000-0000-0000-0000-000000000000",
                    "displayName": "Sub1"},
                {
                    "subscriptionId": "00000000-0000-0000-0000-000000000001",
                    "displayName": "Sub2"
                }
            ],
            "resourceTypes": [
                {"typeName": "vm"},
                {"typeName": "storage"}
            ]
        }]
    }

    def test_cloud_generator(self):
        container = MockBlobStorageSimulator()
        config_generator = CloudConfigGenerator(container)
        config = config_generator.generate_config(
            self.provider_types, self.types)

        # Asserting both string comparison and dictionary comparison
        # just to show serialization/deserialization isn't a problem
        self.assertEqual(config, json.dumps(self.expected_config))
        self.assertDictEqual(json.loads(config), self.expected_config)
