import os

from cloud_scanner.contracts import RuleFactory, register_rule
from .unittest_base import TestCase
from unittest.mock import patch

def create_func():
    return MockRule()

class MockRule:
    pass

class TestRuleFactory(TestCase):
    def setUp(self):
        os.environ["TAG_UPDATES_QUEUE_NAME"] = "resource-tag-updates"
        os.environ["QUEUE_TYPE"] = "simulator"

    def test_get_all_rules(self):
        rules = RuleFactory.get_rules()

        self.assertEqual(4, len(rules))

    @patch.object(RuleFactory, 'register_rule')
    def test_register_rule_decorator(self, register_rule_mock):
        decorator = register_rule(create_func)
        decorator(RuleFactory)

        register_rule_mock.assert_called_once()

    def test_get_rules(self):
        rules = RuleFactory.get_rules()
        self.assertGreater(len(rules), 0)

