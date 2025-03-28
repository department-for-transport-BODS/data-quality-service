from datetime import datetime, timezone
from enums import DQSReportStatus


def get_uk_time():
    """
    Define the UK timezone offset (+0100 for BST, +0000 for GMT)
    """
    return datetime.now(timezone.utc)


def update_dq_report_status(status):
    """
    Update the status of the data quality report.
    Args:
        status (str): The current status of the data quality report.
    Returns:
        str: The updated status of the data quality report.
    """
    return (
        DQSReportStatus.PIPELINE_FAILED.value
        if status == DQSReportStatus.PIPELINE_PENDING.value
        else status
    )
