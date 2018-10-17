import json
import uuid

from cloud_scanner.simulators import TableStorageSimulator, ResourceServiceSimulator
from .unittest_base import TestCase


class TestTableStorage(TestCase):

    def test_entry_is_inserted(self):

        storage_table = TableStorageSimulator()
        resource_service = ResourceServiceSimulator()
        resources = resource_service.get_resources()

        for resource in resources:
            resource_raw = resource.to_str()
            data = json.loads(resource_raw)

            # insert the entry onto Cosmos
            storage_table.write(resource)

            # for data in datastore:
            location = data['location']

            # save partition and row key for access later
            partition_key = location
            row_key = str(uuid.uuid3(uuid.NAMESPACE_DNS, data['id']))

            # verify the entry was written to the table
            retrieved_entry = None
            retrieved_entry = storage_table.query(partition_key, row_key)

            # verify the entry was inserted on Cosmos
            self.assertIsNotNone(retrieved_entry, "No entry was inserted on Cosmos")

            # delete the entry for good practice
            storage_table.delete(partition_key, row_key)
