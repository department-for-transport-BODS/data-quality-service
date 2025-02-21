from dqs_logger import logger
from task_results import TaskResult
from dqs_report import DQReport
from enums import DQSTaskResultStatus, DQSReportStatus
from monitor_utils import  map_pipeline_status, send_sqs_messages
import pandas as pd
from utils import update_dq_report_status


def lambda_handler(event, context):
    """
    AWS Lambda function to handle data quality service errors and update the status of data quality reports and tasks.
    Args:
        event (dict): The event data passed to the Lambda function, expected to contain a "revision_id".
        context (object): The context in which the Lambda function is called.
    Returns:
        None
    Raises:
        ValueError: If no DQ report or tasks are found for the given revision_id.
    Logs:
        Logs various stages of the process, including errors, warnings, and info messages.
    Workflow:
        1. Logs the incoming event.
        2. Checks for the presence of "revision_id" in the event.
        3. Retrieves the data quality report for the given revision_id.
        4. Retrieves the task results associated with the data quality report.
        5. Updates the status of the task results to "FAILED".
        6. Updates the status of the data quality report based on the task results.
        7. Sends SQS messages for the updated data quality report.
        8. Handles and logs any exceptions that occur during the process.
        9. Ensures SQS messages are sent in the finally block.
    """
    logger.info(f"Error occurred in lambda_handler with event: {event}")

    try:
        df_generate_csv = pd.DataFrame()
        revision_id = event.get("revision_id")
        if not revision_id:
            logger.error("Revision ID is required for TopLevelErrorHandler")
            raise ValueError("Revision ID is required for TopLevelErrorHandler")
        
        
        dq_report_instance = DQReport()
        dq_report = dq_report_instance.get_dq_report_by_revision_id(revision_id, DQSReportStatus.PIPELINE_PENDING.value)
        if dq_report.empty:
            logger.warning(f"No DQ report found for revision_id: {revision_id}")
            raise ValueError(f"No DQ report found for revision_id: {revision_id}")

        dq_report_id = dq_report['id'].tolist()
        task_result_instance = TaskResult(dq_report_id)
        tasks = task_result_instance.get_task_results_df()
        if tasks.empty:
            logger.warning(f"No tasks found for dq_report_id: {dq_report_id}")
            dq_report['status'] = dq_report['status'].apply(update_dq_report_status)
            dq_report_instance.update_dq_reports_status_using_ids(dq_report)
            raise ValueError(f"No tasks found for dq_report_id: {dq_report_id}")

        task_result_instance.update_task_results_status_using_ids(DQSTaskResultStatus.FAILED.value)
        tasks['status'] = tasks['status'].apply(lambda x: DQSTaskResultStatus.FAILED.value if x == DQSTaskResultStatus.PENDING.value else x)
        tasks = tasks[['dataquality_report_id', 'status']].drop_duplicates()
        dq_report_with_status = tasks.groupby(["dataquality_report_id"])[["status"]].apply(map_pipeline_status, include_groups=False).reset_index()
        dq_report_with_status = dq_report_with_status.rename(columns={'pipeline_status': 'status'})
        dq_report_with_status.rename(columns={"dataquality_report_id":"id"}, inplace=True)
        dq_report_with_status = dq_report_with_status[["id", "status"]].drop_duplicates().reset_index(drop=True)
        
        df_generate_csv = dq_report_with_status[dq_report_with_status['status'].isin([DQSReportStatus.PIPELINE_SUCCEEDED.value, DQSReportStatus.PIPELINE_SUCCEEDED_WITH_ERRORS.value])]
        logger.info(f"Pending tasks found for dq_report_id: {dq_report_id}")
        logger.info(f"Pending tasks: {tasks}")
        
        send_sqs_messages(df_generate_csv)
        dq_report_instance.update_dq_reports_status_using_ids(dq_report_with_status)

    except Exception as e:
        logger.error(f"Error occurred in lambda_handler: {e}")
        logger.exception(e)

    finally:
        logger.info("lambda_handler completed successfully.")


