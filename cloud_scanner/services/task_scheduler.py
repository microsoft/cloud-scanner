import json
import logging

from cloud_scanner.contracts import CloudConfigReader
from cloud_scanner.contracts.queue_factory import QueueFactory
from cloud_scanner.contracts.storage_container_factory import StorageContainerFactory
from cloud_scanner.config.process_config import ProcessConfig


class TaskScheduler:

    @staticmethod
    def execute():

        queue_name = ProcessConfig().task_queue_name

        task_queue = QueueFactory.create(queue_name)
        storage_container = StorageContainerFactory.create()
        config_reader = CloudConfigReader(storage_container)
        cloud_config = config_reader.read_config()

        for provider in cloud_config["providers"]:
            tasks = TaskScheduler._create_tasks(provider["type"], provider)

            task_count = 0

            for task in tasks:
                logging.info(f"Pushing task {task} to queue {queue_name}")
                task_queue.push(json.dumps(task))
                task_count += 1

        return task_count

    @staticmethod
    def _create_tasks(provider_type: str, config):
        tasks = []
        # put the tasks in the queue
        for subscription in config['subscriptions']:
            # handle the scenario where no resource type is specified
            if config['resourceTypes'] is None:
                sub_id = subscription['subscriptionId']

                data = {
                    'providerType': provider_type,
                    'subscriptionId': sub_id
                }
                message = json.dumps(data)
                tasks.append(message)

            for resource_type in config['resourceTypes']:
                sub_id = subscription['subscriptionId']
                r_type = resource_type['typeName']

                data = {
                    'providerType': provider_type,
                    'subscriptionId': sub_id,
                    'typeName': r_type
                }

                tasks.append(data)

        return tasks
