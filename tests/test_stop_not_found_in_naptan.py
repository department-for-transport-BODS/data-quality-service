from unittest.mock import MagicMock, patch
import pandas as pd
from src.template.stop_not_found_in_naptan import lambda_handler, lambda_worker
from tests.test_templates import lambda_invalid_check


@patch("src.template.stop_not_found_in_naptan.Check")
@patch("src.template.stop_not_found_in_naptan.ObservationResult")
@patch("src.template.stop_not_found_in_naptan.get_df_vehicle_journey")
@patch("src.template.stop_not_found_in_naptan.get_naptan_availablilty")
def test_lambda_handler_valid_check(
    mock_get_naptan_availablilty, mock_get_df_non_naptan_vehicle_journey, mock_observation, mock_check, mocked_context
):
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observation = mock_observation.return_value
    mocked_observation.add_observation = MagicMock()
    mocked_observation.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()
    mocked_observation.observations = [1, 3, 4]
    mock_get_df_non_naptan_vehicle_journey.return_value = pd.DataFrame(
        {
            "is_timing_point": [True, False, True],
            "vehicle_journey_id": [1, 2, 3],
            "sequence_number": [1, 2, 3],
            "activity": ["setDown", "pickUp", "setDownDriverRequest"],
            "atco_code": ["123", "456", "789"],
            "naptan_stop_id": [None, "1", "2"],
            "common_name": ["Stop A", "Stop B", "Stop C"],
            "start_time": ["10:00", "11:00", "12:00"],
            "direction": ["North", "South", "East"],
            "service_pattern_stop_id": [101, 102, 103],
        }
    )
    lambda_worker(None, mocked_check)

    assert mock_get_df_non_naptan_vehicle_journey.called
    assert mock_get_naptan_availablilty.called
    assert mocked_observation.add_observation.call_count == 1
    mocked_observation.add_observation.assert_called_with(
        details="The Stop A (123) stop is not registered with NaPTAN. Please check the ATCO code is correct or contact your local authority to register this stop with NaPTAN.",
        vehicle_journey_id=1,
        service_pattern_stop_id=101,
    )
    assert mocked_observation.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")


@patch("src.template.stop_not_found_in_naptan.Check")
@patch("src.template.stop_not_found_in_naptan.ObservationResult")
@patch("src.template.stop_not_found_in_naptan.get_df_vehicle_journey")
@patch("src.template.stop_not_found_in_naptan.get_naptan_availablilty")
def test_lambda_handler_valid_check_case_sensitive(
    mock_get_naptan_availablilty,
    mock_get_df_non_naptan_vehicle_journey,
    mock_observation,
    mock_check,
    mocked_context,
):
    event = {"Records": [{"body": '{"file_id": 40, "check_id": 1, "result_id": 8}'}]}
    context = mocked_context
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observation = mock_observation.return_value
    mocked_observation.add_observation = MagicMock()
    mocked_observation.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()
    mocked_observation.observations = [1, 3, 4]
    mock_get_df_non_naptan_vehicle_journey.return_value = pd.DataFrame(
        {
            "is_timing_point": [True, False, True],
            "vehicle_journey_id": [1, 2, 3],
            "sequence_number": [1, 2, 3],
            "activity": ["setDown", "pickUp", "setDownDriverRequest"],
            "atco_code": ["ndk123", "atcoCode", "789"],
            "naptan_stop_id": [None, "1", "2"],
            "common_name": ["Stop A", "Stop B", "Stop C"],
            "start_time": ["10:00", "11:00", "12:00"],
            "direction": ["North", "South", "East"],
            "service_pattern_stop_id": [101, 102, 103],
        }
    )
    mock_get_naptan_availablilty.return_value = pd.DataFrame(
        {
            "atco_code": ["NDK123", "ATCOCODE", "789"],
            "atco_code_exists": [True, True, True],
        }
    )

    lambda_worker(event, mocked_check)

    assert mock_get_df_non_naptan_vehicle_journey.called
    assert mock_get_naptan_availablilty.called
    assert mocked_observation.add_observation.call_count == 0


@patch("src.template.stop_not_found_in_naptan.Check")
def test_lambda_handler_invalid_check(mock_check, mocked_context):
    lambda_invalid_check(lambda_handler, mock_check, mocked_context)

