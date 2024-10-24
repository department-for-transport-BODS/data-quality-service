from unittest.mock import MagicMock, patch
from src.template.missing_journey_code import lambda_worker
import pandas as pd
from enums import DQSTaskResultStatus


class TestMissingJourneyCode:
    @patch("src.template.missing_journey_code.get_df_vehicle_journey")
    @patch("src.template.missing_journey_code.ObservationResult")
    @patch("src.template.missing_journey_code.Check")
    @patch("src.template.missing_journey_code.logger")
    def test_lambda_handler_success(
        self,
        mock_logger,
        mock_check,
        mock_observation,
        mock_get_df_vehicle_journey,
        mocked_context,
    ):
        event = {
            "Records": [{"body": '{"file_id": 40, "check_id": 1, "result_id": 8}'}]
        }
        context = mocked_context
        mocked_check = mock_check.return_value = MagicMock()
        mocked_check.validate_requested_check = MagicMock()
        mocked_observation = mock_observation.return_value
        mocked_observation.add_observation = MagicMock()
        mocked_observation.write_observations = MagicMock()
        mocked_check.set_status = MagicMock()

        mock_df = pd.DataFrame(
            {
                "is_timing_point": [False, True, True],
                "vehicle_journey_id": [1, 2, 3],
                "sequence_number": [1, 2, 3],
                "activity": ["setDown", "pickUp", "setDownDriverRequest"],
                "common_name": ["Stop A", "Stop B", "Stop C"],
                "start_time": ["10:00", "11:00", "12:00"],
                "direction": ["North", "South", "East"],
                "service_pattern_stop_id": [101, 102, 103],
                "vehicle_journey_code": [None, "XYZ", "ABC"],
            }
        )

        mock_get_df_vehicle_journey.return_value = mock_df

        lambda_worker(event, mocked_check)
        
        mock_get_df_vehicle_journey.assert_called_once()
        mocked_observation.add_observation.assert_called_once_with(
            details="The (10:00) North journey is missing a journey code.",
            vehicle_journey_id=1,
            service_pattern_stop_id=101,
        )
        mocked_check.set_status.assert_called_once_with(
            DQSTaskResultStatus.SUCCESS.value
        )

    @patch("src.template.missing_journey_code.get_df_vehicle_journey")
    @patch("src.template.missing_journey_code.ObservationResult")
    @patch("src.template.missing_journey_code.Check")
    @patch("src.template.missing_journey_code.logger")
    def test_lambda_handler_no_null_codes(
        self,
        mock_logger,
        mock_check,
        mock_observation,
        mock_get_df_vehicle_journey,
        mocked_context,
    ):
        event = {}
        context = mocked_context
        mocked_check = mock_check.return_value
        mocked_check.validate_requested_check.return_value = True
        mocked_observation = mock_observation.return_value
        mocked_observation.add_observation = MagicMock()
        mocked_observation.write_observations = MagicMock()
        mocked_check.set_status = MagicMock()

        mock_df = pd.DataFrame(
            {
                "is_timing_point": [False, True],
                "vehicle_journey_id": [1, 2],
                "sequence_number": [1, 2],
                "activity": ["setDown", "pickUp"],
                "common_name": ["Stop A", "Stop B"],
                "start_time": ["10:00", "11:00"],
                "direction": ["North", "South"],
                "service_pattern_stop_id": [101, 102],
                "vehicle_journey_code": ["ABC", "XYZ"],
            }
        )

        mock_get_df_vehicle_journey.return_value = mock_df

        lambda_worker(event, mocked_check)

        mock_get_df_vehicle_journey.assert_called_once()
        mocked_observation.add_observation.assert_not_called()
        mocked_observation.write_observations.assert_called_once()
        mocked_check.set_status.assert_called_once_with(
            DQSTaskResultStatus.SUCCESS.value
        )

        mock_logger.info.assert_any_call("Check status updated in DB")

    @patch('src.template.missing_journey_code.get_df_vehicle_journey')
    @patch('src.template.missing_journey_code.ObservationResult')
    @patch('src.template.missing_journey_code.Check')
    @patch('src.template.missing_journey_code.logger')
    def test_lambda_handler_empty_df(self, mock_logger, mock_check, mock_observation, mock_get_df_vehicle_journey,mocked_context):
        event = {}
        context = mocked_context
        mocked_check = mock_check.return_value
        mocked_check.validate_requested_check.return_value = True
        mocked_observation = mock_observation.return_value
        mocked_check.set_status = MagicMock()

        mock_get_df_vehicle_journey.return_value = pd.DataFrame()

        lambda_worker(event, mocked_check)

        mock_get_df_vehicle_journey.assert_called_once()
        mocked_observation.add_observation.assert_not_called()
        mocked_observation.write_observations.assert_not_called()
        mocked_check.set_status.assert_called_once_with(DQSTaskResultStatus.FAILED.value)

    @patch('src.template.missing_journey_code.get_df_vehicle_journey')
    @patch('src.template.missing_journey_code.ObservationResult')
    @patch('src.template.missing_journey_code.Check')
    @patch('src.template.missing_journey_code.logger')
    def test_lambda_handler_exception(self, mock_logger, mock_check, mock_observation, mock_get_df_vehicle_journey,mocked_context):
        event = {}
        context = mocked_context 
        mocked_check = mock_check.return_value
        mocked_check.set_status = MagicMock()

        mock_get_df_vehicle_journey.side_effect = Exception("Test Exception")

        lambda_worker(event, mocked_check)

        mocked_check.set_status.assert_called_once_with(DQSTaskResultStatus.FAILED.value)
        mock_logger.error.assert_called_once_with("Check status failed due to Test Exception")
