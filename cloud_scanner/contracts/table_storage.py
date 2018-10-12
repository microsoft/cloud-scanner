from abc import ABC, abstractmethod


class TableStorage(ABC):

    @abstractmethod
    def write(self, entry):
        raise NotImplementedError("Should have implemented write_entry")

    def write_entries(self, entries):
        for entry in entries:
            self.write(entry)

    @abstractmethod
    def query_list(self) -> list:
        raise NotImplementedError("Should have implemented query_list")

    @abstractmethod
    def query(self, partition_key, row_key):
        raise NotImplementedError("Should have implemented query")

    @abstractmethod
    def delete(self, partition_key, row_key):
        raise NotImplementedError("Should have implemented delete")
