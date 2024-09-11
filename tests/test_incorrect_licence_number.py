from unittest.mock import MagicMock, patch
from src.template.incorrect_licence_number import lambda_handler

@patch("src.template.incorrect_licence_number.Check")
@patch("src.template.incorrect_licence_number.ObservationResult")
@patch("src.template.incorrect_licence_number.OrganisationTxcFileAttributes")
def test_lambda_handler_valid_check(
    mock_txc_attributes,
    mock_observation,
    mock_check,
    mocked_context
):
    event = {"Records": [{"body": '{"file_id": 363, "check_id": 1, "result_id": 5}'}]}
    context = mocked_context
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
    lambda_handler(event, context)
    assert mocked_check.validate_requested_check.called
    assert mocked_observations.add_observation.call_count == 0
    # assert mocked_observations.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")

    # Scenario - Where the licence number is invalid
    mocked_txc_attributes.validate_licence_number.return_value = False
    mocked_txc_attributes.licence_number = "INVALIDLICENCE"
    lambda_handler(event, context)
    assert mocked_check.validate_requested_check.called
    assert mocked_observations.add_observation.call_count == 1
    mocked_observations.add_observation.assert_called_with(
        details="The Licence Number INVALIDLICENCE does not match the Licence Number(s) registered to your BODS organisation profile.",
    )
    assert mocked_observations.write_observations.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")