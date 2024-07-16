from os import environ
import boto3
from dqs_logger import logger

class SQSClient:
    def __init__(self):
        self.endpoint_url = environ.get("SQS_QUEUE_ENDPOINT", "")
        self._sqs_client = boto3.client(
            "sqs", endpoint_url=self.endpoint_url
        )

    def get_sqs_queue_url(self, queue_name):
        try:
            response = self._sqs_client.get_queue_url(QueueName=queue_name)
            return response['QueueUrl']
        except self._sqs_client.exceptions.QueueDoesNotExist:
            logger.error(f"Queue with name {queue_name} does not exist.")
            raise
        except Exception as e:
            logger.error(f"Error getting queue URL: {e}")
            raise

    def send_messages_batch(self, queue_url, entries):
        try:
            response = self._sqs_client.send_message_batch(
                QueueUrl=queue_url,
                Entries=entries
            )
            return response
        except Exception as e:
            logger.error(f"Error sending messages in batch: {e}")
            raise
