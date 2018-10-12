import re


class ResourceExtractors:

    """
    Utility class for extracting components from an Azure Resource id

    Attributes:
        provider_extractor: Regex for extracting the resource provider.
        type_extractor: Regex for extracting types from a resource provider.
        rg_sub_extractor: Regex for extracting the resource group and subscription id.
    """

    provider_extractor = re.compile(r"(?!(?:\/[^\/]+\/[^\/]+)+\/providers)\/providers\/([^\/]+)((:?\/[^\/]+\/[^\/]+)*)$", re.IGNORECASE)
    type_extractor = re.compile(r"\/([^\/]+)\/([^\/]+)", re.IGNORECASE)
    rg_sub_extractor = re.compile(r"\/subscriptions\/([^\/\s]+)(?:\/resourceGroups\/([^\/\s]+))?", re.IGNORECASE)

    @classmethod
    def get_subscription(cls, resource_id):
        """
        Extracts the subscription id from a resource id.
        :param resource_id" resource id to extract from
        :return: subscription id string or None
        """

        matches = cls.rg_sub_extractor.search(resource_id)
        if matches is None:
            return None

        return matches.group(1)

    @classmethod
    def get_resource_group(cls, resource_id):
        """
        Extracts the resource group from a resource id.
        :param resource_id" resource id to extract from
        :return: resource group string or None
        """

        matches = cls.rg_sub_extractor.search(resource_id)
        if matches is None:
            return None

        return matches.group(2)

    @classmethod
    def get_resource_provider(cls, resource_id):
        """
        Extracts the resource provider from a resource id.
        :param resource_id" resource id to extract from
        :return: resource provider string or None
        """

        ms_resource_id = "/providers/Microsoft.Resources" + resource_id

        provider_matches = cls.provider_extractor.search(ms_resource_id)
        if provider_matches is None:
            return None

        return provider_matches.group(1)

    @classmethod
    def get_resource_type(cls, resource_id):
        """
        Extracts the resource type from a resource id.
        :param resource_id" resource id to extract from
        :return: resource type string or None
        """
        ms_resource_id = "/providers/Microsoft.Resources" + resource_id

        provider_matches = cls.provider_extractor.search(ms_resource_id)
        if provider_matches is None:
            return None

        partial_type = provider_matches.group(1)
        resources = provider_matches.group(2)

        for type_match in cls.type_extractor.finditer(resources):
            type_token = type_match.group(1)
            partial_type += "/" + type_token

        return partial_type
