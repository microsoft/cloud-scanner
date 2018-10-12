from abc import ABC, abstractmethod


class ResourceFilter(ABC):
    @abstractmethod
    def normalized_filter(self):
        raise NotImplementedError("normalized_filter is not implemented")


class ResourceService(ABC):
    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError("name is not implemented")

    @abstractmethod
    def get_resources(self, filter: ResourceFilter=None):
        raise NotImplementedError("get_resources is not implemented")

    @abstractmethod
    def get_filter(self, payload) -> ResourceFilter:
        raise NotImplementedError('get_filter is not implemented')

    @abstractmethod
    def update_resource(self, resource):
        raise NotImplementedError("update_resource is not implemented")
