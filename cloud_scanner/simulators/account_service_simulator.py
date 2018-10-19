from cloud_scanner.contracts import AccountService, register_account_service


@register_account_service("simulator", lambda: AccountServiceSimulator())
class AccountServiceSimulator(AccountService):
    """Simulator of AccoutService."""

    def get_accounts(self):
        """Get fake accounts.

        :return: List of fake accounts
        [
            {
                'subscriptionId': '...',
                'displayName': '...'
            },
            ...
        ]
        """
        return [
            {
                "subscriptionId": "00000000-0000-0000-0000-000000000000",
                "displayName": "Sub1"
            },
            {
                "subscriptionId": "00000000-0000-0000-0000-000000000001",
                "displayName": "Sub2"
            }
        ]
