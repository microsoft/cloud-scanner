from abc import ABC


class AccountService(ABC):
    """Service to retrieve account information for cloud provider."""

    def get_accounts(self):
        """
        :return: list of accounts from cloud provider
        """
        raise NotImplementedError("accounts is not implemented")
