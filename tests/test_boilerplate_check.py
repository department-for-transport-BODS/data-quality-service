from src.boilerplate.common import Check
from unittest.mock import patch
from pytest import raises
from json import loads, dumps
from pydantic_core import ValidationError
from types import SimpleNamespace
from .mock_db import MockedDB
from sqlalchemy import select


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

def test_invalid_result_record():
    mock_db = MockedDB()
    test_task_result = mock_db.classes.data_quality_taskresult(
        id = 2,
        checks_id = 1,
        status = "PENDING",
        transmodel_txcfileattributes_id = 50
    )
    mock_db.session.add(test_task_result)
    mock_db.session.flush()
    check = Check(SAMPLE_SQS_EVENT)
    with patch.object(check, "_db", new=mock_db):
        with raises(ValueError):
            check.validate_requested_check()

def test_invalid_result_status():
    mock_db = MockedDB()
    test_task_result = mock_db.classes.data_quality_taskresult(
        id = 1,
        checks_id = 1,
        status = "ERROR",
        transmodel_txcfileattributes_id = 50
    )
    mock_db.session.add(test_task_result)
    mock_db.session.flush()
    check = Check(SAMPLE_SQS_EVENT)
    with patch.object(check, "_db", new=mock_db):
        with raises(ValueError):
            check.validate_requested_check()

def test_null_result_status():
    mock_db = MockedDB()
    test_task_result = mock_db.classes.data_quality_taskresult(
        id = 1,
        checks_id = 1,
        status = None,
        transmodel_txcfileattributes_id = 50
    )
    mock_db.session.add(test_task_result)
    mock_db.session.flush()
    check = Check(SAMPLE_SQS_EVENT)
    with patch.object(check, "_db", new=mock_db):
        with raises(ValueError):
            check.validate_requested_check()

def test_valid_check_record():
    mock_db = MockedDB()
    test_task_result = mock_db.classes.data_quality_taskresult(
        id = 1,
        checks_id = 1,
        status = "PENDING",
        transmodel_txcfileattributes_id = 50
    )
    mock_db.session.add(test_task_result)
    mock_db.session.flush()
    print(mock_db.session.scalars(select(mock_db.classes.data_quality_taskresult)).one().id)
    check = Check(SAMPLE_SQS_EVENT)
    with patch.object(check, "_db", new=mock_db):
        assert check.validate_requested_check()



