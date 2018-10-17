from abc import ABC

from .resource import Resource


class Rule(ABC):
    """Interface of a rule.

    Any implemented rule must define each method described in this
    interface.
    """

    def check_condition(self, resource: Resource) -> bool:
        """Returns True/False whether the rule should be performed on the input
        resource.

        :param resource: The resource to check if the rule should be ran upon.
        :return: Boolean if the resource should be processed with the rule.
        """
        raise NotImplementedError(
            "check_condition is not implemented in the abstract base class")

    def process(self, resource: Resource) -> bool:
        """Processes the resource with the rule.

        :param resource: The resource to be processed with the rule.
        :return: Boolean if the rule had any effect.
        """
        raise NotImplementedError(
            "check_condition is not implemented in the abstract base class")
