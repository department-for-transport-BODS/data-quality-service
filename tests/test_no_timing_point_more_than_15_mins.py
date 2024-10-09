from unittest.mock import MagicMock, patch
import pandas as pd
from src.template.no_timing_point_for_more_than_15_minutes import lambda_worker


@patch("src.template.no_timing_point_for_more_than_15_minutes.Check")
@patch("src.template.no_timing_point_for_more_than_15_minutes.ObservationResult")
@patch("src.template.no_timing_point_for_more_than_15_minutes.get_df_vehicle_journey")
def test_lambda_handler_valid_check(
    mock_get_df_vehicle_journey, mock_observation, mock_check, mocked_context
):
    event = {"Records": [{"body": '{"file_id": 40, "check_id": 14, "result_id": 8}'}]}
    context = mocked_context
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()
    mocked_observations.observations = [1, 3, 4]
    df = pd.read_csv(
        "tests/data/no_timing_point_for_more_than_15_minutes/timing_point.csv"
    )
    df["departure_time"] = pd.to_datetime(
        df["departure_time"], format="%H:%M:%S"
    ).dt.time
    df["start_time"] = pd.to_datetime(df["start_time"], format="%H:%M:%S").dt.time
    mock_get_df_vehicle_journey.return_value = df
    lambda_worker(event, context, mocked_check)

    
    assert mock_get_df_vehicle_journey.called
    assert mocked_observations.add_observation.call_count == 1
    mocked_observations.add_observation.assert_called_with(
        details="The link between the 05:41 Nottingham Railway Station (3390S4) and 06:04 County Hall (3300RU0003) timing point stops on the 05:40 outbound journey is more than 15 minutes apart. The Traffic Commissioner recommends services to have timing points no more than 15 minutes apart.",
        vehicle_journey_id=34554,
        service_pattern_stop_id=536303,
    )
    assert mocked_observations.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")
