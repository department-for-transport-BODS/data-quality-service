def lambda_invalid_check(lambda_handler, mock_check, mocked_context):
    mocked_check = mock_check.return_value
    mocked_check.validate_requested_check.side_effect = ValueError(
        "Invalid Check Error"
    )

    lambda_handler(None, mocked_context)

    assert mocked_check.validate_requested_check.called
    assert mocked_check.set_status.called
    mocked_check.set_status.assert_called_with("FAILED")
