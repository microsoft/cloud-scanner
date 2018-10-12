import logging

from cloud_scanner.contracts.resource import Resource
from cloud_scanner.contracts.resource_service import ResourceService
from cloud_scanner.contracts.resource_service_factory import ResourceServiceFactory
from cloud_scanner.contracts.resource_storage_factory import ResourceStorageFactory
from cloud_scanner.contracts.rule_factory import RuleFactory


class ResourceTagger:

    @staticmethod
    def process_queue_message(message):
        msg_json = message.get_json()
        table_storage = ResourceStorageFactory.create()

        resource = Resource(msg_json["resource"])
        resource_service = ResourceServiceFactory.create(resource.provider_type, resource.account_id)

        tag_processor = ResourceTagProcessor(resource_service)

        tag_processor.execute(resource, msg_json["tags"])
        table_storage.write(resource)

        return tag_processor.tags_written, tag_processor.tags_skipped

    @staticmethod
    def process_tag_rules():
        resource_storage = ResourceStorageFactory.create()
        resources = resource_storage.query_list()
        rules = RuleFactory.get_rules()

        processed_matches = 0

        for resource in resources:
            for rule in rules:
                if rule.process(resource):
                    processed_matches += 1

        return processed_matches


class ResourceTagProcessor:
    def __init__(self, resource_service: ResourceService):
        self._resource_service = resource_service
        self._tags_written = 0
        self._tags_skipped = 0

    @property
    def tags_written(self):
        return self._tags_written

    @property
    def tags_skipped(self):
        return self._tags_skipped

    def execute(self, resource: Resource, tags: dict, overwrite=False):
        # Store tags written during this single execution
        local_written = 0

        for tag_key, tag_value in tags.items():
            if not overwrite and tag_key in resource.tags:
                logging.info(
                    f"Skipped tagging {resource.id} with tag {tag_key} since it already exists.")
                self._tags_skipped += 1
                continue

            resource.tags[tag_key] = tag_value
            local_written += 1
            self._tags_written += 1

        # Only save if needed
        if local_written > 0:
            self._resource_service.update_resource(resource)
            logging.info(f"Wrote {self._tags_written} tags to {resource.id}.")

    def reset(self):
        self._tags_written = 0
        self._tags_skipped = 0
