import datetime
from os import environ
from unittest.mock import patch, MagicMock

from freezegun import freeze_time
import pandas as pd
import pytest

from src.boilerplate.common import Check, DQReport
from src.boilerplate.enums import DQ_Task_Result_Status
from src.monitor.app import lambda_handler
from tests.test_boilerplate_db import ENVIRONMENT_INPUT_TEST_VALUES
from tests.utils import modify_date_columns

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@pytest.mark.parametrize(
        "folder, task_result_ids",
        [
        ("pending_and_timeout", [5]),
        ("empty_dq_report",[]),
        ("empty_task_results",[])
        ]
)
@patch("src.boilerplate.common.Check.update_task_results_status_using_ids")
@patch("src.boilerplate.common.DQReport.update_dq_reports_status_using_ids")
@patch("src.boilerplate.common.DQReport.get_dq_reports_by_status")
@patch("src.boilerplate.common.Check.get_task_results_df")
@patch.dict(environ, ENVIRONMENT_INPUT_TEST_VALUES)
@freeze_time("2024-05-22 15:37:29")
def test_pipeline_for_pending_and_timeout(mock_get_task_results_df, mock_get_dq_reports_by_status, mock_update_dq_reports_status_using_ids, mock_update_task_results_status_using_ids, folder,  task_result_ids):

    csv_dq_reports = pd.read_csv(f"tests/monitor/data/{folder}/dq_report.csv")
    csv_task_reports = pd.read_csv(f"tests/monitor/data/{folder}/dq_task_result.csv")
    csv_output = pd.read_csv(f"tests/monitor/data/{folder}/output.csv")

    if not csv_dq_reports.empty:
        csv_dq_reports = modify_date_columns(csv_dq_reports, ["created"])

    if not csv_task_reports.empty:    
        csv_task_reports = modify_date_columns(csv_task_reports, ["created"])

    mock_get_dq_reports_by_status.return_value = csv_dq_reports
    mock_get_task_results_df.return_value = csv_task_reports
 
    lambda_handler(None, None)

    df_mocked_dq_reports = mock_update_dq_reports_status_using_ids.call_args[0][0]
    pd.testing.assert_frame_equal(df_mocked_dq_reports, csv_output)
    mock_update_task_results_status_using_ids.assert_called_with(task_result_ids, DQ_Task_Result_Status.TIMEOUT, 'pipeline_monitor')