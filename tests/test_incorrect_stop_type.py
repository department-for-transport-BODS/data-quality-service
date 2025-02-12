from unittest.mock import MagicMock, patch
import pandas as pd
from src.template.incorrect_stop_type import lambda_handler, lambda_worker
from tests.test_templates import lambda_invalid_check


@patch("src.template.incorrect_stop_type.Check")
@patch("src.template.incorrect_stop_type.ObservationResult")
@patch("src.template.incorrect_stop_type.get_df_stop_type")
def test_lambda_handler_valid_check(
    mock_get_df_stop_type,
    mock_observation,
    mock_check
):
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
    lambda_worker(None, mocked_check)

    
    assert mock_get_df_stop_type.called
    assert mocked_observations.add_observation.call_count == 3
    mocked_observations.add_observation.assert_called_with(
        details="The Stop C (3290YYA00526) stop is registered as stop type BST with NaPTAN. Expected bus stop types are BCT, BCQ, BCS, BCE or BST.",
        vehicle_journey_id=3,
        service_pattern_stop_id=103,
    )

    assert mocked_observations.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")


@patch("src.template.incorrect_stop_type.Check")
def test_lambda_handler_invalid_check(mock_check,mocked_context):
    lambda_invalid_check(lambda_handler, mock_check, mocked_context)
