import os

from cloud_scanner.simulators import ResourceServiceSimulator
from cloud_scanner.services.resource_tagger import ResourceTagger, ResourceTagProcessor
from .unittest_base import TestCase, FakeQueueMessage


class ResourceTaggerTest(TestCase):
    def setUp(self):
        os.environ["RESOURCE_STORAGE_TYPE"] = "simulator"

    def test_process_queue_message(self):
        os.environ["PROVIDER_LIST"] = "simulator"

        json_data = '''
            {
                "resource": {
                    "id": "00000000-0000-0000-0000-000000000123",
                    "type": "vm",
                    "group": "MyGroup",
                    "name": "MyResource",
                    "location": "WestUS",
                    "providerType": "simulator",
                    "accountId": "00000000-0000-0000-0000-000000000001"
                },
                "tags": {
                    "a": "1",
                    "b": "2"
                }
            }
        '''
        message = FakeQueueMessage(bytes(json_data, 'utf-8'))
        result = ResourceTagger.process_queue_message(message)

        self.assertEqual(2, result[0])
        self.assertEqual(0, result[1])

    def test_scanner_multiple_write(self):
        target_tags = {
            'tag1': 'value',
            'tag2': 'value'
        }

        resource_service = ResourceServiceSimulator()
        tag_processor = ResourceTagProcessor(resource_service)

        resource = resource_service.get_resources()[0]

        tag_processor.execute(resource, target_tags, True)

        assert(tag_processor.tags_written == 2)
        assert(tag_processor.tags_skipped == 0)

    def test_scanner_overwrite(self):
        test_tag_name = 'testTag1'
        test_tag_value = 'testTag1Value'
        test_tag_default_value = 'default'

        target_tags = dict()
        target_tags[test_tag_name] = test_tag_value

        resource_service = ResourceServiceSimulator()
        tag_processor = ResourceTagProcessor(resource_service)

        resource = resource_service.get_resources()[0]

        # Test does overwrite

        resource.tags = target_tags.copy()
        resource.tags[test_tag_name] = test_tag_default_value

        tag_processor.execute(resource, target_tags, True)

        assert(tag_processor.tags_written == 1)
        assert(tag_processor.tags_skipped == 0)
        assert(resource.tags[test_tag_name] == test_tag_value)

        # Test does not overwrite

        resource.tags = target_tags.copy()
        resource.tags[test_tag_name] = test_tag_default_value

        tag_processor.reset()
        tag_processor.execute(resource, target_tags, False)

        assert(tag_processor.tags_written == 0)
        assert(tag_processor.tags_skipped == 1)
        assert(resource.tags[test_tag_name] == test_tag_default_value)

    def test_process_rules(self):
        os.environ["TAG_UPDATES_QUEUE_NAME"] = "resource-tag-updates"
        os.environ["QUEUE_TYPE"] = "simulator"


        processed = ResourceTagger.process_tag_rules()

        self.assertEqual(10, processed)
