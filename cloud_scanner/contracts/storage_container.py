from abc import ABC, abstractmethod


class StorageContainer(ABC):

    @abstractmethod
    def upload_text(self, filename, text):
        raise NotImplementedError("Should have implemented upload_text")

    @abstractmethod
    def list_blobs(self):
        raise NotImplementedError("Should have implemented push")

    @abstractmethod
    def get_blob_to_text(self, file):
        raise NotImplementedError("Should have implemented pop")
