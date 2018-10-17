import json

from .rule import Rule
from .queue import Queue
from .resource import Resource


class TagUpdateRule(Rule):
    """Utility base class for a rule that will update the tags on a given
    resource. Any tag update will be pushed onto a queue with a message
    containing the resource and a dictionary of tags to append.

    Attributes:
        _queue: An instance of the queue to push the tag update message to.
    """

    def __init__(self, queue: Queue):
        """Initializes the rule with a specified queue to push the tag changes
        to."""
        self._queue = queue

    def process(self, resource: Resource):
        """Processes the resource with the rule. The resource will first be
        checked to see the rule should be run using 'check_condition'.

        :param resource: The resource to be processed with the rule.
        :return: Boolean if the rule was run.
        """
        if self.check_condition(resource):
            tags = self.get_tags(resource)
            payload = {
                "resource": resource.to_dict(),
                "tags": tags
            }

            self._queue.push(json.dumps(payload))
            return True

        return False

    def get_tags(self, resource: Resource) -> dict:
        """The dictionary of tags to update the resource with.

        :param resource: The resource to update tags on.
        :return: dict of tags as key value pairs.
        """
        raise NotImplementedError(
            "get_tags is not implemented in the abstract base class")
