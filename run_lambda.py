from src.template.incorrect_noc import lambda_handler
from json import dumps

lambda_handler(
    event={
        "Records": [{"body": dumps(obj={"file_id": 1, "check_id": 1, "result_id": 1})}]
    },
    context=None,
)
