from cloud_scanner.contracts import (
    TableStorage, Resource, register_resource_storage)
from cloud_scanner.helpers import entry_storage


@register_resource_storage("simulator",
                           lambda: TableStorageSimulator())
class TableStorageSimulator(TableStorage):
    """Simulator of TableStorage service."""

    def __init__(self):
        self._data = dict()

        self._resources = [
            {"id": '/resources/type1/resource1',
             "accountId": "account1",
             "type": "Microsoft.Storage/virtualMachine",
             "name": "resource1",
             "providerType": "simulator",
             "location": "location1"},
            {"id": '/resources/type1/resource2',
             "accountId": "account2",
             "type": "Microsoft.Storage/virtualMachine",
             "name": "resource2",
             "providerType": "simulator",
             "location": "location2"},
            {"id": '/resources/type1/resource3',
             "accountId": "account2",
             "type": "Microsoft.Storage/virtualMachine",
             "name": "resource3",
             "providerType": "simulator",
             "location": "location3"},
            {"id": '/resources/type1/resource4',
             "accountId": "account3",
             "type": "Microsoft.Storage/virtualMachine",
             "name": "resource4",
             "providerType": "simulator",
             "location": "location4"},
            {"id": '/resources/type1/resource5',
             "accountId": "account4",
             "type": "Microsoft.Storage/virtualMachine",
             "name": "resource5",
             "providerType": "simulator",
             "location": "location5"},
        ]

    # entry is of json type
    def write(self, resource):
        """Write resource to storage.

        :param resource: Resource to write
        :return: None
        """
        entry = resource.to_dict()
        prepared = entry_storage.EntryOperations.prepare_entry_for_insert(
            entry)
        key = entry['PartitionKey'] + '-' + entry['RowKey']
        self._data[key] = prepared

    def query(self, partition_key, row_key):
        """Get element from table storage.

        :param partition_key: Partition key of resource
        :param row_key: Row key of resource
        :return: Resource if found
        """
        task = self._data[partition_key + '-' + row_key]
        return task

    def query_list(self):
        """Get all resources in storage.

        :return: List of Resource objects
        """
        return [Resource(resource) for resource in self._resources]

    def delete(self, partition_key, row_key):
        """Delete resource from storage.

        :param partition_key: Partition key of resource
        :param row_key: Row key of resource
        :return: None
        """
        del self._data[partition_key + '-' + row_key]
