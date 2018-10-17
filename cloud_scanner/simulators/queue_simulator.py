import collections

from cloud_scanner.contracts.queue import Queue
from cloud_scanner.contracts.queue_factory import register_queue_service


@register_queue_service("simulator", lambda queue_name: QueueSimulator(queue_name))
class QueueSimulator(Queue):
    """
    Simulator of queue service
    """

    def __init__(self, queue_name, config=None):
        self._queue_name = queue_name
        self._queue = collections.deque()

    def __len__(self):
        return len(self._queue)

    def push(self, message):
        """
        Push new message to queue
        :param message: message to push
        :return: None
        """
        self._queue.append(message)

    def pop(self):
        """
        Pop message off of queue
        :return: Message popped
        """
        return self._queue.popleft()

    def peek(self):
        """
        Peek at message, but don't pop
        :return: Message peeked
        """
        return self._queue[0]
