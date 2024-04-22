from src.boilerplate.common import Check
from unittest.mock import patch
from pytest import raises
from json import loads, dumps
from pydantic_core import ValidationError
from types import SimpleNamespace


SAMPLE_SQS_EVENT = {
    "Records": [
        {
            "body": dumps(
                {
                    "txc_file_id": 50,
                    "check_id": 1
                }
            )
        }
    ]
}

MALFORMED_SQS_EVENT = {
    "Records": [
        {
            "body": dumps(
                {
                    "txc_id": 50
                }
            )
        }
    ]
}

def test_check_details_extraction():
    check = Check(SAMPLE_SQS_EVENT)
    assert check.file_id == 50
    assert check.check_id == 1

    check2 = Check(SAMPLE_SQS_EVENT)
    assert check2.check_id == 1
    assert check2.file_id == 50

def test_check_details_failed_extraction(caplog):
    check = Check(MALFORMED_SQS_EVENT)
    with raises(ValidationError):
        file_id = check.file_id
    assert "Failed to extract a valid payload" in caplog.text

@patch('src.boilerplate.common.BodsDB')
def test_get_task_result_id(db):
    db.return_value.session.query.return_value.filter.return_value.all.return_value = [SimpleNamespace(id=1)]
    check = Check(SAMPLE_SQS_EVENT)
    assert check.task_result_id == 1

@patch('src.boilerplate.common.BodsDB')
def test_get_no_task_result_id(db, caplog):
    db.return_value.session.query.return_value.filter.return_value.all.return_value = []
    check = Check(SAMPLE_SQS_EVENT)
    with raises(ValueError):
        id = check.task_result_id
    assert "no record waiting" in caplog.text

@patch('src.boilerplate.common.BodsDB')
def test_error_on_task_result_id(db, caplog):
    db.return_value.session.query.return_value.filter.return_value.all.side_effect = Exception()
    check = Check(SAMPLE_SQS_EVENT)
    with raises(Exception):
        id = check.task_result_id
    assert "failed to get record" in caplog.text


