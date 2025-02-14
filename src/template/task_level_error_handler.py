from dqs_logger import logger
from task_results import TaskResult
from dqs_report import DQReport
from enums import DQSTaskResultStatus, DQSReportStatus, Timeouts
from dataframes import update_taskresult_status


def lambda_handler(event, context):
    logger.info(f"Error occurred in lambda_handler with event: {event}")
    revision_id = event.get("revision_id")
    file_id = event.get("file_id")
    observation = event.get("observation")

    report = DQReport()
    if observation:
        update_taskresult_status(report, revision_id, file_id,None, DQSReportStatus.PIPELINE_FAILED.value)