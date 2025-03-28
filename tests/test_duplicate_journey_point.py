from os.path import dirname
from unittest.mock import MagicMock, patch
import pandas as pd
from src.template.duplicate_journey_code import lambda_worker, lambda_handler
from tests.test_templates import lambda_invalid_check
from tests.fixtures.context import mocked_context  # noqa


@patch("src.template.duplicate_journey_code.Check")
@patch("src.template.duplicate_journey_code.ObservationResult")
@patch("src.template.duplicate_journey_code.get_vj_duplicate_journey_code")
def test_lambda_handler_valid_check(
    mock_get_vj_duplicate_journey_code, mock_observation, mock_check
):
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()
    mocked_observations.observations = [1, 2, 3]
    mock_get_vj_duplicate_journey_code.return_value = pd.read_json(
        f"{dirname(__file__)}/data/duplicate_journey_codes/one_jc_duplicate.json"
    )
    lambda_worker(None, mocked_check)

    assert mock_get_vj_duplicate_journey_code.called
    assert mocked_observations.add_observation.call_count == 2
    mocked_observations.add_observation.assert_called_with(
        details="The Journey Code (1025) is found in more than one vehicle journey.",
        vehicle_journey_id=1941,
        service_pattern_stop_id=18713060,
    )
    assert mocked_observations.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")


@patch("src.template.duplicate_journey_code.Check")
@patch("src.template.duplicate_journey_code.ObservationResult")
@patch("src.template.duplicate_journey_code.get_vj_duplicate_journey_code")
def test_lambda_handler_multiple_duplicates(
    mock_get_vj_duplicate_journey_code, mock_observation, mock_check
):
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()
    mocked_observations.observations = [1, 3, 4]
    dataframe = pd.read_json(
        f"{dirname(__file__)}/data/duplicate_journey_codes/multiple_vjc_duplicates.json"
    )
    mock_get_vj_duplicate_journey_code.return_value = dataframe
    lambda_worker(None, mocked_check)

    assert mock_get_vj_duplicate_journey_code.called
    assert mocked_observations.add_observation.call_count == 4
    mocked_observations.add_observation.assert_called_with(
        details="The Journey Code (1425) is found in more than one vehicle journey.",
        vehicle_journey_id=1943,
        service_pattern_stop_id=18713187,
    )
    assert mocked_observations.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")


@patch("src.template.duplicate_journey_code.Check")
@patch("src.template.duplicate_journey_code.ObservationResult")
@patch("src.template.duplicate_journey_code.get_vj_duplicate_journey_code")
def test_lambda_handler_no_duplicates(
    mock_get_vj_duplicate_journey_code, mock_observation, mock_check
):
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()
    mock_get_vj_duplicate_journey_code.return_value = pd.read_json(
        f"{dirname(__file__)}/data/duplicate_journey_codes/vjc_no_duplicates.json"
    )
    lambda_worker(None, mocked_check)

    assert mock_get_vj_duplicate_journey_code.called
    assert mocked_observations.add_observation.call_count == 0
    assert not mocked_observations.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")


@patch("src.template.duplicate_journey_code.Check")
@patch("src.template.duplicate_journey_code.ObservationResult")
@patch("src.template.duplicate_journey_code.get_vj_duplicate_journey_code")
def test_lambda_handler_no_journies(
    mock_get_vj_duplicate_journey_code, mock_observation, mock_check
):
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()
    mock_get_vj_duplicate_journey_code.return_value = pd.DataFrame()
    lambda_worker(None, mocked_check)

    assert mock_get_vj_duplicate_journey_code.called
    assert mocked_observations.add_observation.call_count == 0
    assert not mocked_observations.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")


@patch("src.template.duplicate_journey_code.Check")
@patch("src.template.duplicate_journey_code.ObservationResult")
@patch("src.template.duplicate_journey_code.get_vj_duplicate_journey_code")
def test_lambda_handler_different_operating_profile(
    mock_get_vj_duplicate_journey_code, mock_observation, mock_check
):
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()
    mock_get_vj_duplicate_journey_code.return_value = pd.read_json(
        f"{dirname(__file__)}/data/duplicate_journey_codes/duplicate_with_different_operating_profile.json"
    )
    lambda_worker(None, mocked_check)

    assert mock_get_vj_duplicate_journey_code.called
    assert mocked_observations.add_observation.call_count == 0
    assert not mocked_observations.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")


@patch("src.template.duplicate_journey_code.Check")
def test_lambda_handler_invalid_check(mock_check, mocked_context):
    lambda_invalid_check(lambda_handler, mock_check, mocked_context)
