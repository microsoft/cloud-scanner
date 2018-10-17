from abc import ABC, abstractmethod


class StorageContainer(ABC):
    """Base class for storage container."""

    @abstractmethod
    def upload_text(self, filename, text):
        """Upload text to file in storage container Not implemented in this
        class."""
        raise NotImplementedError("Should have implemented upload_text")

    @abstractmethod
    def list_blobs(self):
        """Get list of files in storage container Not implemented in this
        class."""
        raise NotImplementedError("Should have implemented push")

    @abstractmethod
    def get_blob_to_text(self, file):
        """Get text content from file in storage container Not implemented in
        this class."""
        raise NotImplementedError("Should have implemented pop")
