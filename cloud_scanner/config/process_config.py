from .configuration import Config


class ProcessConfig(Config):
    """Configuration of workflow names, types and other process-specific
    info."""

    @property
    def task_queue_name(self):
        """Gets the name of the task queue Specified by the TASK_QUEUE_NAME
        property."""
        return self.get_property('TASK_QUEUE_NAME')

    @property
    def payload_queue_name(self):
        """Gets the name of the payload queue Specified by the
        PAYLOAD_QUEUE_NAME property."""

        return self.get_property('PAYLOAD_QUEUE_NAME')

    @property
    def config_container_name(self):
        """Gets the name of the config container Specified by the
        CONFIG_CONTAINER property."""
        return self.get_property('CONFIG_CONTAINER')

    @property
    def tag_updates_queue_name(self):
        """Gets the name of queue used for tag updates Specified by the
        TAG_UPDATES_QUEUE_NAME property."""
        return self.get_property('TAG_UPDATES_QUEUE_NAME')

    @property
    def queue_type(self):
        """Gets the type of queue currently being used Specified by the
        QUEUE_TYPE property.

        Acceptable values:     'azure_storage_queue'
        """
        return self.get_property('QUEUE_TYPE')

    @property
    def storage_container_type(self):
        """Gets the type of storage container currently being used Specified by
        the STORAGE_CONTAINER_TYPE property.

        Acceptable values:     'azure_storage'
        """
        return self.get_property('STORAGE_CONTAINER_TYPE')

    @property
    def resource_storage_type(self):
        """Gets the type of resource storage currently being used Specified by
        the RESOURCE_STORAGE_TYPE property.

        Acceptable values:     'elastic_search'     'azure_cosmos_table'
        'mysql'     'rest_storage_service' (REST_STORAGE_URL must also
        be specified)
        """
        return self.get_property('RESOURCE_STORAGE_TYPE')

    @property
    def rest_storage_url(self):
        """Gets the URL for the Rest storage service if being used Specified by
        the REST_STORAGE_URL property."""
        return self.get_property("REST_STORAGE_URL")

    @property
    def batch_size(self):
        """Gets the batch size of resources to send to the storage service,
        specified by the RESOURCE_BATCH_SIZE property Defaults to 16."""
        return int(self.get_property('RESOURCE_BATCH_SIZE', '16'))
