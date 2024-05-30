
from os import environ
import boto3

class SQSClient:
    def __init__(self):
        self.sqs_resource = boto3.resource('sqs', region_name=environ.get("AWS_REGION","eu-west-2"))


    def get_sqs_queue(self, queue_name):
        return self.sqs_resource.get_queue_by_name(QueueName=queue_name)
    

    def send_messages(self, entries, queue):
        queue.send_messages(Entries=entries)