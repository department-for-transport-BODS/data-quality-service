from unittest.mock import MagicMock, patch
import pandas as pd
from src.template.last_stop_is_pick_up_only import lambda_handler, lambda_worker


@patch("src.template.last_stop_is_pick_up_only.get_df_vehicle_journey")
@patch("src.template.last_stop_is_pick_up_only.ObservationResult")
@patch("src.template.last_stop_is_pick_up_only.Check")
def test_lambda_handler_valid_check(
    mock_check,
    mock_observation,
    mock_get_df_vehicle_journey,
    mocked_context
):
    event = {"Records": [{"body": '{"file_id": 40, "check_id": 1, "result_id": 8}'}]}
    context = mocked_context
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()
    mocked_observations.observations = [1, 3, 4]
    mock_get_df_vehicle_journey.return_value = pd.DataFrame(
        {
            "vehicle_journey_id": [1, 2, 3],
            "sequence_number": [1, 2, 3],
            "activity": ["setDown", "pickUp", "setDownDriverRequest"],
            "common_name": ["Stop A", "Stop B", "Stop C"],
            "start_time": ["10:00", "11:00", "12:00"],
            "direction": ["North", "South", "East"],
            "service_pattern_stop_id": [101, 102, 103],
            "auto_sequence_number": [1, 2, 3],
        }
    )
    lambda_worker(event, context, mocked_check)

    
    assert mock_get_df_vehicle_journey.called
    assert mocked_observations.add_observation.call_count == 1
    mocked_observations.add_observation.assert_called_with(
        details="The last stop (Stop B) on the 11:00 South journey is incorrectly set to pick up passengers.",
        vehicle_journey_id=2,
        service_pattern_stop_id=102,
    )
    assert mocked_observations.write_observations.called
    assert mocked_observations.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")


@patch("src.template.last_stop_is_pick_up_only.Check")
def test_lambda_handler_invalid_check(mock_check, mocked_context):
    event = {"Records": [{"body": '{"file_id": 40, "check_id": 1, "result_id": 8}'}]}
    context = mocked_context
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = False

    lambda_handler(event, context)

    assert mocked_check.validate_requested_check.called
