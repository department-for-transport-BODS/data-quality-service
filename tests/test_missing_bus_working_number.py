from unittest.mock import MagicMock, patch
import pandas as pd
from src.template.missing_bus_working_number import lambda_worker

@patch("src.template.missing_bus_working_number.Check")
@patch("src.template.missing_bus_working_number.ObservationResult")
@patch("src.template.missing_bus_working_number.get_df_missing_bus_working_number")
def test_lambda_handler_valid_check(
    mock_get_df_missing_bus_block_number, mock_observation, mock_check, mocked_context
):
    event = {"Records": [{"body": '{"file_id": 40, "check_id": 14, "result_id": 8}'}]}
    context = mocked_context
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observation = mock_observation.return_value = MagicMock()
    mocked_observation.add_observation = MagicMock()
    mocked_observation.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()
    mock_get_df_missing_bus_block_number.return_value = pd.read_json(
        "tests/data/missing_bus_working_number/missing_bus_working_numbers.json",
        convert_dates=False, # This is to prevent pandas from converting the time to a timestamp
    )
    lambda_worker(event, mocked_check)

    
    assert mock_get_df_missing_bus_block_number.called
    assert mocked_observation.add_observation.call_count == 2
    mocked_observation.add_observation.assert_any_call(
        details="The (09:00) inbound journey has not been assigned a bus working number (i.e. block number).",
        vehicle_journey_id=123,
        service_pattern_stop_id=23344,
    )
    mocked_observation.add_observation.assert_any_call(
        details="The (10:00) outbound journey has not been assigned a bus working number (i.e. block number).",
        vehicle_journey_id=456,
        service_pattern_stop_id=55665,
    )
    mocked_observation.write_observations.assert_called()
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")