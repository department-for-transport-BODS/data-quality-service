from unittest.mock import MagicMock, patch
from src.template.cancelled_service_incorrectly_appearing_as_active import lambda_worker, lambda_handler
from tests.test_templates import lambda_invalid_check


@patch(
    "src.template.cancelled_service_incorrectly_appearing_as_active.OtcInactiveService"
)
@patch("src.template.cancelled_service_incorrectly_appearing_as_active.OtcService")
@patch("src.template.cancelled_service_incorrectly_appearing_as_active.Check")
@patch(
    "src.template.cancelled_service_incorrectly_appearing_as_active.ObservationResult"
)
@patch(
    "src.template.cancelled_service_incorrectly_appearing_as_active.OrganisationTxcFileAttributes"
)
def test_lambda_handler_valid_pass_check(
    mock_txc_attributes,
    mock_observation,
    mock_check,
    mock_otc_service,
    mock_otc_inactive_service,
    mocked_context
):
    mocked_check = mock_check.return_value = MagicMock()
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()

    # Scenario - service code starts with UZ -- UZ000COMM:B1777 -- PASS
    mocked_txc_attributes = mock_txc_attributes.return_value
    mocked_txc_attributes.service_code = "UZ000COMM:B1777"
    lambda_worker(None, mocked_check)
    assert mocked_observations.add_observation.call_count == 0
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")

    # # Scenario - service code present in active -- PF0007157:1 -- PASS
    mocked_txc_attributes.service_code = "PF0007157:1"
    mocked_otc_service = mock_otc_service.return_value
    mocked_otc_service.is_service_exists.return_value = True
    lambda_worker(None, mocked_check)
    assert mocked_observations.add_observation.call_count == 0
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")

    # Scenario - not present in active & present in inactive -- PASS
    mocked_txc_attributes.service_code = "PF2006130:37"
    mocked_otc_service = mock_otc_service.return_value
    mocked_otc_service.is_service_exists.return_value = False
    mocked_otc_inactive_service = mock_otc_inactive_service.return_value
    mocked_otc_inactive_service.is_service_exists.return_value = True
    lambda_worker(None, mocked_check)
    assert mocked_observations.add_observation.call_count == 0
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")


@patch(
    "src.template.cancelled_service_incorrectly_appearing_as_active.OtcInactiveService"
)
@patch("src.template.cancelled_service_incorrectly_appearing_as_active.OtcService")
@patch("src.template.cancelled_service_incorrectly_appearing_as_active.Check")
@patch(
    "src.template.cancelled_service_incorrectly_appearing_as_active.ObservationResult"
)
@patch(
    "src.template.cancelled_service_incorrectly_appearing_as_active.OrganisationTxcFileAttributes"
)
def test_lambda_handler_valid_pass_check_coach(
    mock_txc_attributes,
    mock_observation,
    mock_check,
    mock_otc_service,
    mock_otc_inactive_service,
    mocked_context,
):
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()

    # Scenario - not present in both -- PD1073423:4234 -- FAIL
    mocked_txc_attributes = mock_txc_attributes.return_value
    mocked_txc_attributes.service_code = "PD1073423:4234"
    mocked_txc_attributes.service_mode = "coach"
    mocked_otc_service = mock_otc_service.return_value
    mocked_otc_service.is_service_exists.return_value = False
    mocked_otc_inactive_service = mock_otc_inactive_service.return_value
    mocked_otc_inactive_service.is_service_exists.return_value = False
    lambda_worker(None, mocked_check)
    assert mocked_observations.add_observation.call_count == 0

    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")


@patch(
    "src.template.cancelled_service_incorrectly_appearing_as_active.OtcInactiveService"
)
@patch("src.template.cancelled_service_incorrectly_appearing_as_active.OtcService")
@patch("src.template.cancelled_service_incorrectly_appearing_as_active.Check")
@patch(
    "src.template.cancelled_service_incorrectly_appearing_as_active.ObservationResult"
)
@patch(
    "src.template.cancelled_service_incorrectly_appearing_as_active.OrganisationTxcFileAttributes"
)
def test_lambda_handler_valid_fail_check(
    mock_txc_attributes,
    mock_observation,
    mock_check,
    mock_otc_service,
    mock_otc_inactive_service,
    mocked_context
):
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.return_value = True
    mocked_observations = mock_observation.return_value
    mocked_observations.add_observation = MagicMock()
    mocked_observations.write_observations = MagicMock()
    mocked_check.set_status = MagicMock()

    # Scenario - not present in both -- PD1073423:4234 -- FAIL
    mocked_txc_attributes = mock_txc_attributes.return_value
    mocked_txc_attributes.service_code = "PD1073423:4234"
    mocked_otc_service = mock_otc_service.return_value
    mocked_otc_service.is_service_exists.return_value = False
    mocked_otc_inactive_service = mock_otc_inactive_service.return_value
    mocked_otc_inactive_service.is_service_exists.return_value = False
    lambda_worker(None, mocked_check)
    assert mocked_observations.add_observation.call_count == 1
    mocked_observations.add_observation.assert_called_with(
        details="The registration number (i.e. service code) PD1073423:4234 is not registered with a local bus registrations authority.",
    )
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("SUCCESS")

@patch("src.template.cancelled_service_incorrectly_appearing_as_active.Check")
def test_lambda_handler_invalid_check(mock_check, mocked_context):
    lambda_invalid_check(lambda_handler, mock_check, mocked_context)
