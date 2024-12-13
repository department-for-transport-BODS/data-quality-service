from boto3 import client
from botocore.exceptions import ClientError
from dqs_logger import logger

class S3Client:

    def __init__(self):
        self._s3_client = client(
            "s3"
        )

    def object_exists(self, bucket, key):
        try:
            self._s3_client.head_object(Bucket=bucket, Key=key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            logger.error(f"Error checking if object exists: {e}")
            raise
        except self._s3_client.exceptions.NoSuchKey as e:
            if e.response['Error']['Code'] == '404':
                return False
            logger.error(f"Error checking if object exists: {e}")
            raise

    def put_object(self, bucket, key, data):
        try:
            self._s3_client.put_object(Bucket=bucket, Key=key, Body=data)
        except Exception as e:
            logger.error(f"Error putting object: {e}")
            raise

    def get_object(self, bucket, key):
        try:
            return self._s3_client.get_object(Bucket=bucket, Key=key).get("Body").read()
        except Exception as e:
            logger.error(f"Error getting object: {e}")
            raise