from os import environ
from unittest.mock import patch, MagicMock

from freezegun import freeze_time
import pandas as pd

from src.boilerplate.common import Check, DQReport
from src.monitor.app import lambda_handler
from tests.test_boilerplate_db import ENVIRONMENT_INPUT_TEST_VALUES
from tests.utils import modify_date_columns

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@patch("src.boilerplate.common.DQReport.get_dq_reports_by_status")
@patch("src.boilerplate.common.Check.get_task_results_df")
@patch.dict(environ, ENVIRONMENT_INPUT_TEST_VALUES)
@freeze_time("2024-05-22 15:37:29")
def test_pipeline_for_pending_and_timeout(mock_get_dq_reports_by_status, mock_get_task_results_df):
    logger.info(f"start---")
    check = Check()
    dq_report_instance = DQReport()

    check.update_task_results_status_using_ids = MagicMock()
    dq_report_instance.update_dq_reports_status_using_ids = MagicMock()

    csv_dq_reports = pd.read_csv("tests/monitor/data/pending_and_timeout_dq_report.csv")
    csv_task_reports = pd.read_csv("tests/monitor/data/pending_and_timeout_dq_task_result.csv")

    csv_dq_reports = modify_date_columns(csv_dq_reports, ["created"])
    csv_task_reports = modify_date_columns(csv_task_reports, ["created"])

    mock_get_dq_reports_by_status.return_value = csv_dq_reports
    mock_get_task_results_df.return_value = csv_task_reports
 
    print(f"before---")
    handler = lambda_handler(None, None)
    print(f"handler---{handler}")