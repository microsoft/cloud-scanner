import json
from datetime import datetime

from .account_service_factory import AccountServiceFactory
from .storage_container import StorageContainer


class CloudConfigGenerator:
    """Generate cloud configuration file for process workflow."""

    def __init__(self, storage_container: StorageContainer):
        self._container = storage_container

    def generate_config(self, providers_types: list, resource_types: list):
        """Generate cloud configuration payload.

        :param providers_types:
            comma-separated list of cloud providers (azure, aws, gcp)
        :param resource_types: comma-separated list of cloud resource types
        :return: str of Json payload
        """
        providers = []

        for provider_type in providers_types:
            account_service = AccountServiceFactory.create(provider_type)
            accounts = []
            for account in account_service.get_accounts():
                accounts.append({
                    "subscriptionId": account["subscriptionId"],
                    "displayName": account["displayName"]
                })

            types = []
            for resource_type in resource_types:
                types.append({
                    "typeName": resource_type
                })

            providers.append({
                "type": provider_type,
                "subscriptions": accounts,
                "resourceTypes": types
            })

        return json.dumps({
            "providers": providers
        })

    def output_config(self, config):
        """Upload config payload to Storage container.

        :param config: json payload of config
        :return: None
        """
        blob_name = 'config-{date:%Y-%m-%d-%H-%M-%S}.json'.format(
            date=datetime.now())
        self._container.upload_text(blob_name, config)
