from unittest.mock import MagicMock, patch
from src.template.incorrect_noc import lambda_worker, lambda_handler
from tests.test_templates import lambda_invalid_check
from tests.fixtures.context import mocked_context  # noqa


@patch("src.template.incorrect_noc.Check")
@patch("src.template.incorrect_noc.ObservationResult")
@patch("src.template.incorrect_noc.OrganisationTxcFileAttributes")
def test_lambda_handler_valid_check(
    mock_txc_attributes, mock_observation, mock_check, mocked_context
):
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()
    mocked_observations.observations = [1, 3, 4]

    mocked_txc_attributes = mock_txc_attributes.return_value
    # Scenario - Where the noc code is valid
    mocked_txc_attributes.validate_noc_code.return_value = True
    mocked_txc_attributes.org_noc = "VALIDNOC"
    lambda_worker(None, mocked_check)

    assert mocked_observations.add_observation.call_count == 0
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")

    # Scenario - Where the noc code is in-valid
    mocked_txc_attributes.validate_noc_code.return_value = False
    mocked_txc_attributes.org_noc = "INVALIDNOC"
    lambda_worker(None, mocked_check)

    assert mocked_observations.add_observation.call_count == 1
    mocked_observations.add_observation.assert_called_with(
        details="The National Operator Code INVALIDNOC does not match the NOC(s) registered to your BODS organisation profile.",
    )
    assert mocked_observations.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")


@patch("src.template.incorrect_noc.Check")
def test_lambda_handler_invalid_check(mock_check, mocked_context):
    lambda_invalid_check(lambda_handler, mock_check, mocked_context)
