from os import environ
import logging
import os

import pandas as pd

from src.boilerplate.common import Check, DQReport, EventDetails
from src.boilerplate.enums import DQ_Report_Status, DQ_Task_Result_Status
from src.monitor.utils import map_pipeline_status


logger = logging.getLogger(__name__)
logger.setLevel(environ.get("LOG_LEVEL", "DEBUG"))


def lambda_handler(event, context):
    logger.info("Starting the monitor pipeline lambda function.")
    dq_report_instance = DQReport()
    dq_reports = dq_report_instance.get_dq_reports_by_status(DQ_Report_Status.PIPELINE_PENDING, 'pipeline_monitor')
    logger.info(f"dq_reports---{dq_reports}")
    now = pd.Timestamp.now(tz='UTC')
    timeout_hours = now - pd.Timedelta(hours=os.getenv('TIMEOUT_HOURS', 12))

    dq_report_timeouts = dq_reports[dq_reports['created'] < timeout_hours]
    dq_report_timeout_ids = dq_report_timeouts['id'].to_list()

    # Filter out the timed out records to avoid iterating over its respective task results
    filtered_dq_reports = dq_reports[~dq_reports['id'].isin(dq_report_timeout_ids)]
    filtered_report_ids = filtered_dq_reports['id'].to_list()

    logger.info("Filtered reports based on timeout field.")

    check = Check()
    dq_reports_with_status = pd.DataFrame()
    if filtered_report_ids:
        task_results: pd.DataFrame = check.get_task_results_df(filtered_report_ids, 'pipeline_monitor')
        unique_results = task_results[['dataquality_report_id', 'status']]
        unique_results = unique_results.drop_duplicates()
        dq_reports_with_status = unique_results.groupby(["dataquality_report_id"])[["status"]].apply(map_pipeline_status, include_groups=False).reset_index()
        dq_reports_with_status.rename(columns={"dataquality_report_id":"id"}, inplace=True)

    dq_report_timeouts["status"] = DQ_Report_Status.TIMEOUT
    df_update_dq_reports = pd.concat([dq_reports_with_status, dq_report_timeouts[["id", "status"]]])
    df_update_dq_reports = df_update_dq_reports.rename(columns={'pipeline_status': 'status'})
    df_update_dq_reports = df_update_dq_reports[["id", "status"]].drop_duplicates()

    # dq_report_instance.update_dq_reports_status_using_ids(df_update_dq_reports, 'pipeline_monitor')
    # check.update_task_results_status_using_ids(dq_report_timeout_ids, DQ_Task_Result_Status.TIMEOUT, 'pipeline_monitor')
    logger.info("Monitor pipeline function completed successfully.")