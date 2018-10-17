import uuid


class EntryOperations:
    @staticmethod
    def prepare_entry_for_insert(resource):
        """Optimize resource for table entry insertion.

        :param resource: Resource to be inserted in Storage
        :return: Prepared resource
        """
        # using location as the partition key. This will keep all the data from
        # the same location on the same node for fastest access
        location = resource['location']
        resource['PartitionKey'] = location
        resource['RowKey'] = str(uuid.uuid3(
            uuid.NAMESPACE_DNS, resource['id']))

        # cosmos does not allow for an entry with key 'id'
        modified_data = {}
        for key, value in resource.items():
            if key == 'id':
                modified_data['resourceid'] = str(value)
            else:
                modified_data[key] = str(value)

        return modified_data
