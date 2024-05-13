from src.boilerplate.common import Check
from unittest.mock import patch
from pytest import raises
from json import loads, dumps
from pydantic_core import ValidationError
from types import SimpleNamespace
from .mock_db import MockedDB
from sqlalchemy import select


SAMPLE_SQS_EVENT = {
    "Records": [{"body": dumps({"file_id": 50, "check_id": 1, "result_id": 1})}]
}

MALFORMED_SQS_EVENT = {"Records": [{"body": dumps({"txc_id": 50})}]}


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
    test_task_result = mock_db.classes.data_quality_taskresults(
        id=2, checks_id=1, status="PENDING", transmodel_txcfileattributes_id=50
    )
    mock_db.session.add(test_task_result)
    mock_db.session.flush()
    check = Check(SAMPLE_SQS_EVENT)
    with patch.object(check, "_db", new=mock_db):
        with raises(ValueError):
            check.validate_requested_check()


def test_invalid_result_status():
    mock_db = MockedDB()
    test_task_result = mock_db.classes.data_quality_taskresults(
        id=1, checks_id=1, status="ERROR", transmodel_txcfileattributes_id=50
    )
    mock_db.session.add(test_task_result)
    mock_db.session.flush()
    check = Check(SAMPLE_SQS_EVENT)
    with patch.object(check, "_db", new=mock_db):
        with raises(ValueError):
            check.validate_requested_check()


def test_null_result_status():
    mock_db = MockedDB()
    test_task_result = mock_db.classes.data_quality_taskresults(
        id=1, checks_id=1, status=None, transmodel_txcfileattributes_id=50
    )
    mock_db.session.add(test_task_result)
    mock_db.session.flush()
    check = Check(SAMPLE_SQS_EVENT)
    with patch.object(check, "_db", new=mock_db):
        with raises(ValueError):
            check.validate_requested_check()


def test_valid_check_record():
    mock_db = MockedDB()
    test_task_result = mock_db.classes.data_quality_taskresults(
        id=1, checks_id=1, status="PENDING", transmodel_txcfileattributes_id=50
    )
    mock_db.session.add(test_task_result)
    mock_db.session.flush()
    check = Check(SAMPLE_SQS_EVENT)
    with patch.object(check, "_db", new=mock_db):
        assert check.validate_requested_check()


def test_set_status():
    mock_db = MockedDB()
    test_task_result = mock_db.classes.data_quality_taskresults(
        id=1, checks_id=1, status="PENDING", transmodel_txcfileattributes_id=50
    )
    mock_db.session.add(test_task_result)
    mock_db.session.flush()
    check = Check(SAMPLE_SQS_EVENT)
    with patch.object(check, "_db", new=mock_db):
        check.set_status("SUCCESS")
    assert (
        mock_db.session.scalars(
            select(mock_db.classes.data_quality_taskresults).where(
                mock_db.classes.data_quality_taskresults.id == 1
            )
        )
        .one()
        .status
        == "SUCCESS"
    )


def test_add_observations():
    mock_db = MockedDB()
    test_task_result = mock_db.classes.data_quality_taskresults(
        id=1, checks_id=1, status="PENDING", transmodel_txcfileattributes_id=50
    )
    mock_db.session.add(test_task_result)
    mock_db.session.flush()
    check = Check(SAMPLE_SQS_EVENT)
    with patch.object(check, "_db", new=mock_db):
        check.add_observation(details="No linked values")
        check.add_observation(vehicle_journey_id=1, details="Added Vehicle Journey ID")
        check.add_observation(
            service_pattern_stop_id=1, details="Added Service Pattern Stop ID"
        )
        check.write_observations()
        check.set_status("SUCCESS")
    added_observations = mock_db.session.scalars(
        select(mock_db.classes.data_quality_observationresults)
    ).all()
    assert len(added_observations) == 3
    assert (
        len(
            [
                record
                for record in added_observations
                if record.taskresults_id == 1
                and record.details == "No linked values"
                and record.service_pattern_stop_id is None
                and record.vehicle_journey_id is None
            ]
        )
        == 1
    )
    assert (
        len(
            [
                record
                for record in added_observations
                if record.taskresults_id == 1
                and record.details == "Added Vehicle Journey ID"
                and record.service_pattern_stop_id is None
                and record.vehicle_journey_id == 1
            ]
        )
        == 1
    )
    assert (
        len(
            [
                record
                for record in added_observations
                if record.taskresults_id == 1
                and record.details == "Added Service Pattern Stop ID"
                and record.service_pattern_stop_id == 1
                and record.vehicle_journey_id is None
            ]
        )
        == 1
    )
    for row in added_observations:
        print(row.__dict__)
