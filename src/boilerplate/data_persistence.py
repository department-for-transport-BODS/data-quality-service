from enum import Enum
from os import environ
from pickle import dumps, loads

from dqs_logger import logger
from common import Check
from s3 import S3Client


class PersistenceBackend(str, Enum):

    S3 = "S3"
    REDIS = "REDIS"

class PersistenceKey(str, Enum):

    VEHICLE_JOURNEY = "vehicle_journey"

    def to_check_value(self, check: Check):
        return f"{self.value}-{check.file_id}"

class PersistedData(object):

    def __init__(self):
        backend = environ.get("CACHE_BACKEND")
        if backend == PersistenceBackend.S3:
            self.backend = S3Backend()
        elif backend == PersistenceBackend.REDIS:
            self.backend = RedisBackend()
        else:
            self.backend = None

    def save(self, key, data):
        self.backend.save(key, data) if self.backend else None

    def exists(self, key):
        return self.backend.exists(key) if self.backend else False

    def get(self, key):
        return self.backend.get(key) if self.backend else None

class S3Backend(object):

    def __init__(self):
        self._s3 = S3Client()
        self._bucket = environ.get("CACHE_BUCKET")
        if self._bucket is None:
            raise ValueError("CACHE_BUCKET is not set in environment for S3 Backend Persistence")
        logger.debug(f"Initialised S3 backend using {self._bucket}")

    def save(self, key, data):
        self._s3.put_object(bucket=self._bucket, key=key, data=dumps(data))

    def exists(self, key):
        return self._s3.object_exists(bucket=self._bucket, key=key)

    def get(self, key):
        return loads(self._s3.get_object(bucket=self._bucket, key=key))

class RedisBackend(object):

    def __init__(self):
        logger.error("Redis Backend is not implemented")
        raise ValueError("Redis Backend is not implemented")

    def save(self, key, data):
        pass

    def exists(self, key):
        pass

    def get(self, key):
        pass