from os import environ
import os
from os.path import dirname
from unittest.mock import patch

from freezegun import freeze_time
import pandas as pd
import pytest

from src.boilerplate.enums import DQSTaskResultStatus
from src.template.monitor import lambda_handler
from tests.test_boilerplate_db import ENVIRONMENT_INPUT_TEST_VALUES
from tests.utils import modify_date_columns
from moto import mock_aws
import boto3

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# TODO: Not sure what this is trying to test?

# @pytest.mark.parametrize(
#     "folder, task_result_ids, sqs_msgs",
#     [
#         ("pending_and_timeout", [5], [{"id": 2}, {"id": 3}]),
#         ("empty_dq_report", [], []),
#         ("empty_task_results", [], []),
#     ],
# )
# @patch("src.boilerplate.sqs.SQSClient.send_messages_batch")
# @patch("src.boilerplate.task_results.TaskResult.update_task_results_status_using_ids")
# # @patch("src.boilerplate.common.DQSReport.update_dq_reports_status_using_ids")
# # @patch("src.boilerplate.common.DQSReport.get_dq_reports_by_status")
# @patch("src.boilerplate.task_results.TaskResult.get_task_results_df")
# @patch.dict(environ, ENVIRONMENT_INPUT_TEST_VALUES)
# @freeze_time("2024-05-22 15:37:29")
# @mock_aws
# def test_pipeline_for_pending_and_timeout(mock_get_task_results_df, mock_update_task_results_status_using_ids, mock_send_messages_batch, folder,  task_result_ids, sqs_msgs):
#
#     sqs = boto3.resource('sqs', region_name=os.environ.get("AWS_REGION", 'eu-west-2'))
#     sqs.create_queue(QueueName='local-generate-csv')
#     # csv_dq_reports = pd.read_csv(f"{dirname(__file__)}/data/{folder}/dq_report.csv")
#     csv_task_reports = pd.read_csv(f"{dirname(__file__)}/data/{folder}/dq_task_result.csv")
#     # csv_output = pd.read_csv(f"tests/monitor/data/{folder}/output.csv")
#
#     # if not csv_dq_reports.empty:
#     #     csv_dq_reports = modify_date_columns(csv_dq_reports, ["created"])
#
#     if not csv_task_reports.empty:
#         csv_task_reports = modify_date_columns(csv_task_reports, ["created"])
#
#     # mock_get_dq_reports_by_status.return_value = csv_dq_reports
#     mock_get_task_results_df.return_value = csv_task_reports
#
#     lambda_handler(None, None)
#
#     # df_mocked_dq_reports = mock_update_dq_reports_status_using_ids.call_args[0][0]
#     queue_msgs = mock_send_messages_batch.call_args[0][0]
#
#     assert queue_msgs == sqs_msgs
#     # pd.testing.assert_frame_equal(df_mocked_dq_reports, csv_output)
#     mock_update_task_results_status_using_ids.assert_called_with(task_result_ids, DQSTaskResultStatus.TIMEOUT, 'pipeline_monitor')
