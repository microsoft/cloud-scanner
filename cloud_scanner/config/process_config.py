from .configuration import Config


class ProcessConfig(Config):
    '''
    Configuration of workflow names, types and other process-specific info
    '''

    @property
    def task_queue_name(self):
        '''
        Gets the name of the task queue, specified by the TASK_QUEUE_NAME property.
        '''
        return self.get_property('TASK_QUEUE_NAME')

    @property
    def payload_queue_name(self):
        '''
        Gets the name of the payload queue, specified by the PAYLOAD_QUEUE_NAME property.
        '''

        return self.get_property('PAYLOAD_QUEUE_NAME')

    @property
    def config_container_name(self):
        '''
        Gets the name of the config container, specified by the CONFIG_CONTAINER property.
        '''
        return self.get_property('CONFIG_CONTAINER')

    @property
    def tag_updates_queue_name(self):
        return self.get_property('TAG_UPDATES_QUEUE_NAME')

    @property
    def queue_type(self):
        return self.get_property('QUEUE_TYPE')

    @property
    def storage_container_type(self):
        return self.get_property('STORAGE_CONTAINER_TYPE')

    @property
    def resource_storage_type(self):
        return self.get_property('RESOURCE_STORAGE_TYPE')

    @property
    def rest_storage_url(self):
        return self.get_property("REST_STORAGE_URL")

    @property
    def batch_size(self):
        return int(self.get_property('RESOURCE_BATCH_SIZE', '16'))



