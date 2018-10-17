import json
import logging

from .storage_container import StorageContainer


class CloudConfigReader:
    """Helper to read cloud configuration file."""

    def __init__(self, container_service: StorageContainer):
        self._container_service = container_service

    def read_config(self):
        """Read cloud configuration file from storage container.

        :return: json payload of cloud config
        """
        # get a list of files in the blob container
        config_list = self._container_service.list_blobs()

        # find the most recent config file
        latest_config = "config-"
        for config_filename in config_list:

            if config_filename.name > latest_config:
                latest_config = config_filename.name

        if latest_config == "config-":
            logging.error("Could not find any config files in blob container")
            return None

        # read the contents of the latest config
        json_data = self._container_service.get_blob_to_text(
            latest_config).content
        if json_data == '{}':
            logging.error("Empty JSON returned!")
            return None

        return json.loads(json_data)
