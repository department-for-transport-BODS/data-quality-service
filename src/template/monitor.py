from datetime import datetime
from dqs_logger import logger
import os
import pandas as pd

from task_results import TaskResult
from dqs_report import DQReport
from enums import DQSTaskResultStatus, DQSReportStatus, Timeouts
from monitor_utils import  map_pipeline_status, send_sqs_messages


def lambda_handler(event, context):
    logger.info("Starting the monitor pipeline lambda function.")
    dq_report_instance = DQReport()
    dq_reports = dq_report_instance.get_dq_reports_by_status(DQSReportStatus.PIPELINE_PENDING.value)
    # Overcome issue with Freezegun not freezing date for pd.timestamp.now()
    now = pd.to_datetime(datetime.now(), utc=True)
    timeout_hours = now - pd.Timedelta(hours=os.getenv('TIMEOUT_HOURS', Timeouts.TIMEOUT_HOURS.value))

    dq_report_timeouts = dq_reports[dq_reports['created'] < timeout_hours]
    dq_report_timeout_ids = dq_report_timeouts['id'].to_list()

    # Filter out the timed out records to avoid iterating over its respective task results
    filtered_dq_reports = dq_reports[~dq_reports['id'].isin(dq_report_timeout_ids)]
    filtered_report_ids = filtered_dq_reports['id'].to_list()

    logger.info("Filtered reports based on timeout field.")

    dq_reports_with_status = pd.DataFrame()
    if filtered_report_ids:
        task_result = TaskResult(filtered_report_ids)
        task_results_df: pd.DataFrame = task_result.get_task_results_df()
        unique_results = task_results_df[['dataquality_report_id', 'status']]
        unique_results = unique_results.drop_duplicates()
        dq_reports_with_status = unique_results.groupby(["dataquality_report_id"])[["status"]].apply(map_pipeline_status, include_groups=False).reset_index()
        dq_reports_with_status.rename(columns={"dataquality_report_id":"id"}, inplace=True)

    dq_report_timeouts["status"] = DQSReportStatus.TIMEOUT.value
    df_update_dq_reports = pd.concat([dq_reports_with_status, dq_report_timeouts[["id", "status"]]])
    df_update_dq_reports = df_update_dq_reports.rename(columns={'pipeline_status': 'status'})
    df_update_dq_reports = df_update_dq_reports[["id", "status"]].drop_duplicates()
    df_update_dq_reports.reset_index(drop=True, inplace=True)
    df_generate_csv = df_update_dq_reports[df_update_dq_reports['status'].isin([DQSReportStatus.PIPELINE_SUCCEEDED.value, DQSReportStatus.PIPELINE_SUCCEEDED_WITH_ERRORS.value])]

    send_sqs_messages(df_generate_csv)

    dq_report_instance.update_dq_reports_status_using_ids(df_update_dq_reports)
    try:
        task_result_instance = TaskResult(dq_report_timeout_ids)
        task_result_instance.update_task_results_status_using_ids(DQSTaskResultStatus.TIMEOUT.value)
        logger.info("Task results status updated successfully.")
    except Exception as e:
        logger.info(f"Error updating task results status: {e}")
        logger.exception(e)

    logger.info("Monitor pipeline function completed successfully.")
