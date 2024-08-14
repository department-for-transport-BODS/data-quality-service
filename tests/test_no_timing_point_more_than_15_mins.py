from unittest.mock import MagicMock, patch
import pandas as pd
from src.template.no_timing_point_more_than_15_mins import lambda_handler


@patch("src.template.no_timing_point_more_than_15_mins.Check")
@patch("src.template.no_timing_point_more_than_15_mins.ObservationResult")
@patch("src.template.no_timing_point_more_than_15_mins.get_df_vehicle_journey")
def test_lambda_handler_valid_check(
    mock_get_df_vehicle_journey, mock_observation, mock_check
):
    event = {"Records": [{"body": '{"file_id": 40, "check_id": 14, "result_id": 8}'}]}
    context = {}
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()
    mocked_observations.observations = [1, 3, 4]
    mock_get_df_vehicle_journey.return_value = pd.read_csv(
        "tests/data/no_timing_point_more_than_15_mins/timing_point.csv"
    )
    lambda_handler(event, context)

    assert mocked_check.validate_requested_check.called
    assert mock_get_df_vehicle_journey.called
    assert mocked_observations.add_observation.call_count == 1
    mocked_observations.add_observation.assert_called_with(
        details="Nottingham Railway Station(3390S4) - County Hall(3300RU0003)",
        vehicle_journey_id=34554,
        service_pattern_stop_id=536309,
    )
    assert mocked_observations.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")
