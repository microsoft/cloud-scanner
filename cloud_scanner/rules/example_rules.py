from cloud_scanner.config.process_config import ProcessConfig
from ..contracts.queue_factory import QueueFactory
from ..contracts.resource import Resource
from ..contracts.rule_factory import register_rule
from ..contracts.tag_update_rule import TagUpdateRule


def create_rule(cls):
    queue_name = ProcessConfig().tag_updates_queue_name
    queue = QueueFactory.create(queue_name)
    return cls(queue)


@register_rule(create_rule)
class ExampleRule1(TagUpdateRule):
    def check_condition(self, resource: Resource) -> bool:
        return True if resource.type.startswith("Microsoft.Web") else False

    def get_tags(self, resource: Resource):
        return {"Category": "Azure Web"}


@register_rule(create_rule)
class ExampleRule2(TagUpdateRule):
    def check_condition(self, resource: Resource) -> bool:
        return True if resource.type.startswith("Microsoft.Storage") else False

    def get_tags(self, resource: Resource):
        return {"Category": "Storage"}


@register_rule(create_rule)
class ExampleRule3(TagUpdateRule):
    def check_condition(self, resource: Resource) -> bool:
        return True if "Microsoft" in resource.name else False

    def get_tags(self, resource: Resource):
        return {"Company": "Microsoft"}


@register_rule(create_rule)
class ExampleRule4(TagUpdateRule):
    def check_condition(self, resource: Resource) -> bool:
        return True

    def get_tags(self, resource: Resource):
        return {"Location": resource.location}
