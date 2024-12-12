import logging
import os.path
from unittest.mock import MagicMock, patch
import pandas as pd
from src.template.serviced_organisation_data_is_out_of_date import lambda_handler, lambda_worker

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@patch("src.template.serviced_organisation_data_is_out_of_date.Check")
@patch("src.template.serviced_organisation_data_is_out_of_date.ObservationResult")
@patch("src.template.serviced_organisation_data_is_out_of_date.get_df_serviced_organisation")
def test_lambda_handler_valid_check(
    mock_get_df_serviced_organisation, mock_observation, mock_check, mocked_context
):
    event = {"Records": [{"body": '{"file_id": 40, "check_id": 1, "result_id": 8}'}]}
    context = mocked_context
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()

    df = pd.read_csv(
        f"{os.path.dirname(__file__)}/data/serviced_organisation_data_is_out_of_date/serviced_organisation_one_fail_two_pass.csv"
    )
    df["serviced_organisation_end_date"] = pd.to_datetime(
        df["serviced_organisation_end_date"], format="%Y-%m-%d"
    ).dt.date
    mock_get_df_serviced_organisation.return_value = df

    lambda_worker(event, context)

    # assert mocked_check.validate_requested_check.called
    assert mock_get_df_serviced_organisation.called
    assert mocked_observations.add_observation.call_count == 1
    mocked_observations.add_observation.assert_called_with(
        details="The Working Days for Serviced Organisation Worcester Sixth Form College (WSFC) has expired on 16/12/2022. Please update the dates for this Serviced Organisation.",
        vehicle_journey_id=65271,
        serviced_organisation_vehicle_journey_id=65271
    )
    assert mocked_observations.write_observations.called
    # assert mocked_check.set_status.called
    # mocked_check.set_status.assert_called_with("SUCCESS")


@patch("src.template.serviced_organisation_data_is_out_of_date.Check")
@patch("src.template.serviced_organisation_data_is_out_of_date.ObservationResult")
@patch("src.template.serviced_organisation_data_is_out_of_date.get_df_serviced_organisation")
def test_lambda_handler_valid_check_fails(
    mock_get_df_serviced_organisation, mock_observation, mock_check
):
    event = {"Records": [{"body": '{"file_id": 40, "check_id": 1, "result_id": 8}'}]}
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()

    df = pd.read_csv(
        f"{os.path.dirname(__file__)}/data/serviced_organisation_data_is_out_of_date/serviced_organisation_all_fail.csv"
    )
    df["serviced_organisation_end_date"] = pd.to_datetime(
        df["serviced_organisation_end_date"], format="%Y-%m-%d"
    ).dt.date
    mock_get_df_serviced_organisation.return_value = df

    lambda_worker(event, mocked_check)

    # assert mocked_check.validate_requested_check.called
    assert mock_get_df_serviced_organisation.called
    assert mocked_observations.add_observation.call_count == 3
    mocked_observations.add_observation.assert_any_call(
        details="The Working Days for Serviced Organisation Tenbury High Ormiston Academy (THOA) has expired on 16/12/2022. Please update the dates for this Serviced Organisation.",
        vehicle_journey_id=65164,
        serviced_organisation_vehicle_journey_id=65164
    )
    assert mocked_observations.write_observations.called
    # assert mocked_check.set_status.called
    # mocked_check.set_status.assert_called_with("SUCCESS")


@patch("src.template.serviced_organisation_data_is_out_of_date.Check")
@patch("src.template.serviced_organisation_data_is_out_of_date.ObservationResult")
@patch("src.template.serviced_organisation_data_is_out_of_date.get_df_serviced_organisation")
def test_lambda_handler_valid_check_pass(
    mock_get_df_serviced_organisation: MagicMock, mock_observation, mock_check
):
    event = {"Records": [{"body": '{"file_id": 40, "check_id": 1, "result_id": 8}'}]}
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()
    mocked_check.file_id = 40
    mocked_check.check_id = 1

    df = pd.read_csv(
        f"{os.path.dirname(__file__)}/data/serviced_organisation_data_is_out_of_date/serviced_organisation_all_pass.csv"
    )
    df["serviced_organisation_end_date"] = pd.to_datetime(
        df["serviced_organisation_end_date"], format="%Y-%m-%d"
    ).dt.date
    mock_get_df_serviced_organisation.return_value = df

    lambda_worker(event, mocked_check)

    # assert mocked_check.validate_requested_check.called
    assert mock_get_df_serviced_organisation.called
    assert mocked_observations.add_observation.call_count == 0
    assert mocked_observations.write_observations.called
    # assert mocked_check.set_status.called
    # mocked_check.set_status.assert_called_with("SUCCESS")
