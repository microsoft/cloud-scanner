import os
import logging


def get_enviroment_value(key, default):
    """Gets an enviornment variable value.

    :param key: Name of the environment variable
    :return: The environmeant variable's value or None if it doesn't exist.
    """
    value = os.environ.get(key, default)
    if value is None:
        error_message = f"Env variable {key} is not set"
        logging.error(error_message)
    return value


class Config:
    """Base configuration class.

    Only exposes direct access to get config properties.
    """

    def get_property(self, property_name, default=None):
        """Gets a configuration property.

        :param property_name: The name of the configuration property
        :param default: Default value of property
        :return: The property as a string, or None.
        """

        return get_enviroment_value(property_name, default)
