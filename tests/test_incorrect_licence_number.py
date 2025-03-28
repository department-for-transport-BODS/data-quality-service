from unittest.mock import MagicMock, patch
from src.template.incorrect_licence_number import lambda_worker, lambda_handler
from tests.test_templates import lambda_invalid_check


@patch("src.template.incorrect_licence_number.Check")
@patch("src.template.incorrect_licence_number.ObservationResult")
@patch("src.template.incorrect_licence_number.OrganisationTxcFileAttributes")
def test_lambda_handler_valid_check(
    mock_txc_attributes, mock_observation, mock_check, mocked_context
):
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()

    mocked_txc_attributes = mock_txc_attributes.return_value
    # Scenario - Where the licence number is valid
    mocked_txc_attributes.validate_licence_number.return_value = True
    mocked_txc_attributes.licence_number = "VALIDLICENCE"
    lambda_worker(None, mocked_check)

    assert mocked_observations.add_observation.call_count == 0
    # assert mocked_observations.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")
    mocked_check.set_status.reset_mock()

    mocked_txc_attributes.validate_licence_number.return_value = True
    mocked_txc_attributes.licence_number = "INVALIDLICENCE"
    lambda_worker(None, mocked_check)

    assert mocked_observations.add_observation.call_count == 0
    # assert mocked_observations.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")
    mocked_check.set_status.reset_mock()

    # Scenario - Where the licence number is invalid
    mocked_txc_attributes.validate_licence_number.return_value = False
    mocked_txc_attributes.licence_number = "UZLICENCE"
    lambda_worker(None, mocked_check)

    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")


@patch("src.template.incorrect_licence_number.Check")
def test_lambda_handler_invalid_check(mock_check, mocked_context):
    lambda_invalid_check(lambda_handler, mock_check, mocked_context)
