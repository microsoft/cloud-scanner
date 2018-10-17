def register_rule(factory_func=None):
    """Decorator for registering a rule with the rule factory.

    :param factory_func: Optional lambda/function that will
        create and return an instance of the rule. Required if
        the rule has an __init__ function that takes any parameter
        other than self.
    """
    def decorator(cls):
        if factory_func is None:
            RuleFactory.register_rule(cls)
        else:
            RuleFactory.register_rule(lambda: factory_func(cls))

        return cls
    return decorator


class RuleFactory:
    """Rule factory responsible for maintaining a list of rule
    definitions and returning instances of all registered rules.

    Attributes:
        _rules_factories: A list of lambda/functions that will instantiate
        an instance of each unique rule.
    """
    _rules_factories = []

    @classmethod
    def get_rules(cls) -> list:
        """Returns an instantiated list of each rule that has been registered.

        :return: list[Rule] a list of instantiated rules.
        """
        return [factory() for factory in cls._rules_factories]

    @classmethod
    def register_rule(cls, rule_func):
        """Utility function used by the register_rule decorator to register a
        lambda/function to instantiate a rule."""
        cls._rules_factories.append(rule_func)
