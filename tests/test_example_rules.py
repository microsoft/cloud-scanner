import os

from cloud_scanner.contracts import QueueFactory, Resource
from .unittest_base import TestCase


class TestExampleRules(TestCase):
    def setUp(self):
        os.environ["QUEUE_TYPE"] = "simulator"
        os.environ["TAG_UPDATES_QUEUE_NAME"] = "test-queue-name"
        self._queue = QueueFactory.create("test-queue-name")

        resource_json = { "id": '/resources/type1/resource1', "accountId": "account1", "type": "Microsoft.Storage/virtualMachine", "name": "resource1", "providerType": "simulator", "location": "location1"}
        self._resource = Resource(resource_json)

    def test_rule_1(self):
        from cloud_scanner.rules import ExampleRule1
        rule1 = ExampleRule1(self._queue)
        result = rule1.check_condition(self._resource)
        count = rule1.process(self._resource)

        self.assertFalse(result)
        self.assertEqual(count, 0)

    def test_rule_2(self):
        from cloud_scanner.rules import ExampleRule2
        rule2 = ExampleRule2(self._queue)
        result = rule2.check_condition(self._resource)
        count = rule2.process(self._resource)

        self.assertTrue(result)
        self.assertEqual(count, 1)

    def test_rule_3(self):
        from cloud_scanner.rules import ExampleRule3
        rule3 = ExampleRule3(self._queue)
        result = rule3.check_condition(self._resource)
        count = rule3.process(self._resource)

        self.assertFalse(result)
        self.assertEqual(count, 0)

    def test_rule_4(self):
        from cloud_scanner.rules import ExampleRule4
        rule4 = ExampleRule4(self._queue)
        result = rule4.check_condition(self._resource)
        count = rule4.process(self._resource)

        self.assertTrue(result)
        self.assertEqual(count, 1)




