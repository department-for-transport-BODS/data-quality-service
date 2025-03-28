import unittest
from unittest.mock import patch
from boto3 import client, setup_default_session
from moto import mock_aws
from pandas import DataFrame

from src.boilerplate.data_persistence import PersistedData


class TestBoilerplateDataPersistence(unittest.TestCase):

    valid_s3_environ = dict(
        CACHE_BACKEND="S3",
        CACHE_BUCKET="MyBucket",
        AWS_ACCESS_KEY_ID="SOME_KEY",
        AWS_SECRET_ACCESS_KEY="SOME_SECRET_KEY",
    )
    invalid_s3_environ = dict(CACHE_BACKEND="S3", S3_BUCKET="MyBucket")

    invalid_backend = dict(CACHE_BACKEND="INVALID")
    redis_backend = dict(CACHE_BACKEND="REDIS")

    @patch.dict(
        "src.boilerplate.data_persistence.environ", valid_s3_environ, clear=True
    )
    def test_backend_s3_returns_with_no_errors(self):
        PersistedData()

    @patch.dict(
        "src.boilerplate.data_persistence.environ", invalid_s3_environ, clear=True
    )
    def test_backend_s3_fails_with_no_bucket(self):
        with self.assertRaises(ValueError) as ve:
            PersistedData()
        ex: ValueError = ve.exception
        self.assertEqual(
            ex.__str__(),
            "CACHE_BUCKET is not set in environment for S3 Backend Persistence",
        )

    @patch.dict("src.boilerplate.data_persistence.environ", redis_backend, clear=True)
    def test_invalid_backend_throws_error(self):
        with self.assertRaises(ValueError) as ve:
            PersistedData()
        ex: ValueError = ve.exception
        self.assertEqual(ex.__str__(), "Redis Backend is not implemented")

    @patch.dict("src.boilerplate.data_persistence.environ", invalid_backend, clear=True)
    def test_invalid_backend_has_no_effects(self):
        pd = PersistedData()
        self.assertFalse(pd.exists("Some-Key"))
        pd.save("Some-Key", "Some-Value")
        pd.get("some-key")

    @mock_aws
    @patch.dict(
        "src.boilerplate.data_persistence.environ", valid_s3_environ, clear=True
    )
    def test_save_and_load_pickles_ok(self):
        setup_default_session()
        client("s3", region_name="us-east-1").create_bucket(Bucket="MyBucket")

        pd = PersistedData()
        pd.save("Some-Key", "Some-Value")
        self.assertTrue(pd.exists("Some-Key"))
        self.assertFalse(pd.exists("Some-Other-Key"))
        self.assertEqual(pd.get("Some-Key"), "Some-Value")

    @mock_aws
    @patch.dict(
        "src.boilerplate.data_persistence.environ", valid_s3_environ, clear=True
    )
    def test_retrieval_of_non_existant_key(self):
        setup_default_session()
        client("s3", region_name="us-east-1").create_bucket(Bucket="MyBucket")

        pd = PersistedData()
        pd.save("Some-Key", "Some-Value")

        self.assertFalse(pd.exists("Some-Other-Key"))
        with self.assertRaises(Exception) as ex:
            pd.get("Some-Other-Key")
        e = ex.exception
        self.assertEqual(
            e.__str__(),
            "An error occurred (NoSuchKey) when calling the GetObject operation: The specified key does not exist.",
        )

    @mock_aws
    @patch.dict(
        "src.boilerplate.data_persistence.environ", valid_s3_environ, clear=True
    )
    def test_save_and_load_of_binary_object(self):
        setup_default_session()
        client("s3", region_name="us-east-1").create_bucket(Bucket="MyBucket")

        df = DataFrame(
            {
                "is_timing_point": [True, False, True],
                "vehicle_journey_id": [1, 2, 3],
                "auto_sequence_number": [1, 2, 3],
                "activity": ["setDown", "pickUp", "setDownDriverRequest"],
                "common_name": ["Stop A", "Stop B", "Stop C"],
                "start_time": ["10:00", "11:00", "12:00"],
                "direction": ["North", "South", "East"],
                "service_pattern_stop_id": [101, 102, 103],
            }
        )
        pd = PersistedData()
        pd.save("MyDF", df)
        ldf = pd.get("MyDF")
        self.assertNotEqual(id(ldf), id(df))  # Not the same object returned
        self.assertTrue(df.equals(ldf))  # But the contents are identical
