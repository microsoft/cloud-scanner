from abc import ABC, abstractmethod


class TableStorage(ABC):
    """Base class for Table Storage."""

    @abstractmethod
    def write(self, entry):
        """Write entry to Table Storage Not implemented in this class."""
        raise NotImplementedError("Should have implemented write_entry")

    def write_entries(self, entries):
        """Write collection of entries to Table Storage Not implemented in this
        class."""
        for entry in entries:
            self.write(entry)

    @abstractmethod
    def query_list(self) -> list:
        """Get list of all entries in table storage Not implemented in this
        class."""
        raise NotImplementedError("Should have implemented query_list")

    @abstractmethod
    def query(self, partition_key, row_key):
        """Query Table Storage for specific entry Not implemented in this
        class."""
        raise NotImplementedError("Should have implemented query")

    @abstractmethod
    def delete(self, partition_key, row_key):
        """Delete specific entry in Table Storage Not implemented in this
        class."""
        raise NotImplementedError("Should have implemented delete")
