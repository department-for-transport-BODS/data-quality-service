from unittest.mock import MagicMock, patch
import pandas as pd
from src.template.incorrect_stop_type import lambda_handler


@patch("src.template.incorrect_stop_type.Check")
@patch("src.template.incorrect_stop_type.ObservationResult")
@patch("src.template.incorrect_stop_type.get_df_stop_type")
def test_lambda_handler_valid_check(
    mock_get_df_stop_type,
    mock_observation,
    mock_check,
):
    event = {"Records": [{"body": '{"file_id": 40, "check_id": 1, "result_id": 8}'}]}
    context = {}
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()
    mocked_observations.observations = [1, 3, 4]
    mock_get_df_stop_type.return_value = pd.DataFrame(
        {
            "vehicle_journey_id": [1, 2, 3],
            "sequence_number": [1, 2, 3],
            "activity": ["setDown", "pickUp", "setDownDriverRequest"],
            "common_name": ["Stop A", "Stop B", "Stop C"],
            "start_time": ["10:00", "11:00", "12:00"],
            "direction": ["North", "South", "East"],
            "service_pattern_stop_id": [101, 102, 103],
            "atco_code": ["3290YYA00522", "3290YYA00523", "3290YYA00526"],
            "stop_type": ["AIR", "BCE", "BST"],
        }
    )
    lambda_handler(event, context)

    assert mocked_check.validate_requested_check.called
    assert mock_get_df_stop_type.called
    assert mocked_observations.add_observation.call_count == 3
    mocked_observations.add_observation.assert_any_call(
        details="The Stop A (3290YYA00522) stop is registered as stop type AIR with NaPTAN. Expected bus stop types are BCT, BCQ or BCS.",
        vehicle_journey_id=1,
        service_pattern_stop_id=101,
    )

    mocked_observations.add_observation.assert_any_call(
        details="The Stop B (3290YYA00523) stop is registered as stop type BCE with NaPTAN. Expected bus stop types are BCT, BCQ or BCS.",
        vehicle_journey_id=2,
        service_pattern_stop_id=102,
    )

    mocked_observations.add_observation.assert_any_call(
        details="The Stop C (3290YYA00526) stop is registered as stop type BST with NaPTAN. Expected bus stop types are BCT, BCQ or BCS.",
        vehicle_journey_id=3,
        service_pattern_stop_id=103,
    )
    assert mocked_observations.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")


@patch("src.template.incorrect_stop_type.Check")
def test_lambda_handler_invalid_check(mock_check):
    event = {"Records": [{"body": '{"file_id": 40, "check_id": 1, "result_id": 8}'}]}
    context = {}
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = False

    lambda_handler(event, context)

    assert mocked_check.validate_requested_check.called
