from abc import ABC, abstractmethod


class Queue(ABC):
    """Generic Queue interface.

    Any queue implementation must expose the methods detailed in this
    interface.
    """

    @abstractmethod
    def push(self, message):
        """Pushes a message onto the queue.

        :param message: The message that will be pushed onto the queue
        """
        raise NotImplementedError("Should have implemented push")

    @abstractmethod
    def pop(self):
        """Pops the first message fom the queue and returns it.

        :return: The first message in the queue
        """
        raise NotImplementedError("Should have implemented pop")

    @abstractmethod
    def peek(self):
        """Returns the first message flom the queue, leaving the message in the
        queue.

        :return: First message in the queue
        """
        raise NotImplementedError("Should have implemented peek")
