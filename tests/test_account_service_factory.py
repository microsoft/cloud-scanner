import os

from cloud_scanner.contracts import AccountServiceFactory, AccountService, register_account_service
from unittest.mock import patch
from .unittest_base import TestCase


def create_func():
    return AccountServiceMock()

@register_account_service('test', create_func)
class AccountServiceMock(AccountService):
    pass

class TestAccountServiceFactory(TestCase):
    def test_simulator_account_service(self):
        account_service = AccountServiceFactory.create("simulator")
        self.assertIsNotNone(account_service)
        self.assertEqual(type(account_service).__name__, "AccountServiceSimulator")

    @patch.object(AccountServiceFactory, 'register_factory')
    def test_register_account_service_decorator(self, mock_register_factory):
        decorator = register_account_service('test', create_func)
        decorator(AccountServiceFactory)

        mock_register_factory.assert_called_once_with('test', create_func)

        account_service = AccountServiceFactory.create("test")
        self.assertIsNotNone(account_service)
        self.assertEqual(type(account_service).__name__, "AccountServiceMock")

    def test_unknown_provider(self):
        test_error = None

        try:
            AccountServiceFactory.create("unknown")
        except Exception as create_error:
            test_error = create_error

        self.assertFalse(test_error is None, "Expected error to be thrown for invalid provider")

    def test_get_providers(self):
        providers = AccountServiceFactory.get_providers()
        self.assertGreater(len(providers), 0)


