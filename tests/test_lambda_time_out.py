import pytest
from unittest.mock import MagicMock, patch
from src.boilerplate.time_out_handler import TimeOutHandler, LambdaTimeOutError

@patch("src.boilerplate.time_out_handler.signal")
def test_handle_lambda_timeout(mock_signal):
    context = MagicMock()
    handler = TimeOutHandler(context)
    with pytest.raises(LambdaTimeOutError):
        handler.handle_lambda_timeout(None, None)
    assert mock_signal.alarm.called


@patch("src.boilerplate.time_out_handler.signal")
def test_set_time_out(mock_signal,mocked_context):
    context = mocked_context
    context.get_remaining_time_in_millis.return_value = 17000
    TimeOutHandler(context)
    assert mock_signal.signal.called
    assert mock_signal.alarm.called
    assert context.get_remaining_time_in_millis.called
    mock_signal.alarm.assert_called_with(2)


