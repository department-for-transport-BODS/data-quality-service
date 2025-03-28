import logging
from unittest.mock import MagicMock, patch
import pandas as pd
from src.template.first_stop_is_not_a_timing_point import lambda_handler, lambda_worker
from tests.test_templates import lambda_invalid_check
from tests.fixtures.context import mocked_context  # noqa

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@patch("src.template.first_stop_is_not_a_timing_point.Check")
@patch("src.template.first_stop_is_not_a_timing_point.ObservationResult")
@patch("src.template.first_stop_is_not_a_timing_point.get_df_vehicle_journey")
def test_lambda_handler_valid_check(
    mock_get_df_vehicle_journey, mock_observation, mocked_check, mocked_context
):
    mocked_check = MagicMock()
    mocked_check.validate_requested_check.return_value = True
    mocked_check.set_status = MagicMock()
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_observations.observations = [1, 3, 4]
    mock_get_df_vehicle_journey.return_value = pd.DataFrame(
        {
            "is_timing_point": [False, True, True],
            "vehicle_journey_id": [1, 2, 3],
            "auto_sequence_number": [1, 2, 3],
            "activity": ["setDown", "pickUp", "setDownDriverRequest"],
            "common_name": ["Stop A", "Stop B", "Stop C"],
            "start_time": ["10:00", "11:00", "12:00"],
            "direction": ["North", "South", "East"],
            "service_pattern_stop_id": [101, 102, 103],
        }
    )
    lambda_worker(None, mocked_check)

    assert mock_get_df_vehicle_journey.called
    assert mocked_observations.add_observation.call_count == 1
    mocked_observations.add_observation.assert_called_with(
        details="The first stop (Stop A) on the 10:00 North journey is not set as a timing point.",
        vehicle_journey_id=1,
        service_pattern_stop_id=101,
    )
    assert mocked_observations.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")


@patch("src.template.first_stop_is_not_a_timing_point.Check")
def test_lambda_handler_invalid_check(mock_check, mocked_context):
    lambda_invalid_check(lambda_handler, mock_check, mocked_context)
