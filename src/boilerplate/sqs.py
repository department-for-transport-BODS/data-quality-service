from os import environ
import boto3
from dqs_logger import logger

class SQSClient:
    def __init__(self):
        self._sqs_client = boto3.client(
            "sqs", region_name=environ.get("AWS_REGION", "eu-west-2")
        )

    def get_sqs_queue_url(self, queue_name):
        try:
            response = self._sqs_client.get_queue_url(QueueName=queue_name)
        except self._sqs_client.exceptions.QueueDoesNotExist:
            logger.error(f"Queue with name {queue_name} does not exist.")
            raise
        except Exception as e:
            logger.error(f"Error getting queue URL: {e}")
            raise
        return response['QueueUrl']

    def send_messages_batch(self, queue_url, entries):
        try:
            response = self._sqs_client.send_message_batch(
                QueueUrl=queue_url,
                Entries=entries
            )
            return response
        except Exception as e:
            print(f"Error sending messages in batch: {e}")
            return None
