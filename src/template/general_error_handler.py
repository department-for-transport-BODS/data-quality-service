from dqs_logger import logger
from task_results import TaskResult
from dqs_report import DQReport
from enums import DQSTaskResultStatus, DQSReportStatus, Timeouts
from dqs_top_level_handler_utils import TobLevelErrorHandler

def lambda_handler(event, context):
    logger.info(f"Error occurred in lambda_handler with event: {event}")
    revision_id = event.get("revision_id")
    handler = TobLevelErrorHandler(revision_id)
    reports = handler.get_dq_reports()
    handler.update_dq_reports(reports)



