from json import dumps

SAMPLE_SQS_EVENT = {
    "Records": [{"body": dumps({"file_id": 50, "check_id": 1, "result_id": 1})}]
}
# def test_handler():
#     db = MockedDB()
#     with patch('common.Check.db', db):
#         handler = lambda_handler(SAMPLE_SQS_EVENT, None)
#         print(handler)
