from src.template.app import lambda_handler
from json import dumps
from unittest.mock import patch
from types import SimpleNamespace
from .mock_db import MockedDB

SAMPLE_SQS_EVENT = {
    "Records": [
        {
            "body": dumps(
                {
                    "file_id": 50,
                    "check_id": 1,
                    "result_id": 1
                }
            )
        }
    ]
}
# def test_handler():
#     db = MockedDB()
#     with patch('common.Check.db', db):
#         handler = lambda_handler(SAMPLE_SQS_EVENT, None)
#         print(handler)