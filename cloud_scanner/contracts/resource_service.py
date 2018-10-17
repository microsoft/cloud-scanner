from abc import ABC, abstractmethod


class ResourceFilter(ABC):
    """Base class for a resource filter."""
    @abstractmethod
    def normalized_filter(self):
        """Not implemented in this class."""
        raise NotImplementedError("normalized_filter is not implemented")


class ResourceService(ABC):
    """Base class for resource service."""
    @property
    @abstractmethod
    def name(self):
        """Name of resource service Not implemented in this class."""
        raise NotImplementedError("name is not implemented")

    @abstractmethod
    def get_resources(self, filter: ResourceFilter = None):
        """Get resources based on filter Not implemented in this class."""
        raise NotImplementedError("get_resources is not implemented")

    @abstractmethod
    def get_filter(self, payload) -> ResourceFilter:
        """Get filter object based on payload Not implemented in this class."""
        raise NotImplementedError('get_filter is not implemented')

    @abstractmethod
    def update_resource(self, resource):
        """Update resource within cloud service provider Not implemented in
        this class."""
        raise NotImplementedError("update_resource is not implemented")
