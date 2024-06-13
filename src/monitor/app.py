from datetime import datetime
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as pd

from src.boilerplate.common import Check, DQReport
from src.boilerplate.enums import DQTaskResultStatus, DQReportStatus, Timeouts
from src.monitor.utils import  map_pipeline_status, send_sqs_messages

logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))


def lambda_handler(event, context):
    logger.info("Starting the monitor pipeline lambda function.")
    print("Here")
    dq_report_instance = DQReport()
    dq_reports = dq_report_instance.get_dq_reports_by_status(DQReportStatus.PIPELINE_PENDING, "pipeline_monitor")
    # Overcome issue with Freezegun not freezing date for pd.timestamp.now()
    now = pd.to_datetime(datetime.now(), utc=True)
    timeout_hours = now - pd.Timedelta(hours=os.getenv('TIMEOUT_HOURS', Timeouts.TIMEOUT_HOURS))

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

    dq_report_timeouts["status"] = DQReportStatus.TIMEOUT
    df_update_dq_reports = pd.concat([dq_reports_with_status, dq_report_timeouts[["id", "status"]]])
    df_update_dq_reports = df_update_dq_reports.rename(columns={'pipeline_status': 'status'})
    df_update_dq_reports = df_update_dq_reports[["id", "status"]].drop_duplicates()
    df_update_dq_reports.reset_index(drop=True, inplace=True)
    df_generate_csv = df_update_dq_reports[df_update_dq_reports['status'].isin([DQReportStatus.PIPELINE_SUCCEEDED, DQReportStatus.PIPELINE_SUCCEEDED_WITH_ERRORS])]
    
    send_sqs_messages(df_generate_csv)

    dq_report_instance.update_dq_reports_status_using_ids(df_update_dq_reports, 'pipeline_monitor')
    check.update_task_results_status_using_ids(dq_report_timeout_ids, DQTaskResultStatus.TIMEOUT, 'pipeline_monitor')
    logger.info("Monitor pipeline function completed successfully.")
    