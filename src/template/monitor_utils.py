from os import environ
from dqs_logger import logger
import pandas as pd
import json
from sqs import SQSClient
from enums import DQSTaskResultStatus, DQSReportStatus


def get_generate_csv_queue_name() -> str:
    env = environ.get("PROJECT_ENV", "local")
    if env:
        return f"dqs-{env}-generate-csv-queue"

    return None


def generate_sqs_payload(df: pd.DataFrame) -> list:
    entries = []
    for index, row in df.iterrows():
        entry = {
            "Id": str(row["id"]),
            "MessageBody": json.dumps({"report_id": row["id"]}),
        }
        entries.append(entry)
    return entries


def send_sqs_messages(df: pd.DataFrame):
    sqs_client = SQSClient()
    queue_name = get_generate_csv_queue_name()
    logger.info(f"Getting Queue with name: {queue_name}")
    queue_url = sqs_client.get_sqs_queue_url(queue_name)
    sqs_entries = generate_sqs_payload(df)

    batch_size = 10
    for i in range(0, len(sqs_entries), batch_size):
        batch_entries = sqs_entries[i : i + batch_size]
        response = sqs_client.send_messages_batch(queue_url, batch_entries)
        if response:
            logger.info(f"Batch sent successfully to queue: {queue_name}.")
        else:
            logger.info(f"Failed to send batch to queue: {queue_name}.")


def map_pipeline_status(df: pd.DataFrame) -> pd.DataFrame:
    status = set(df["status"])

    if DQSTaskResultStatus.PENDING.value in status:
        return pd.DataFrame()

    if (DQSTaskResultStatus.SUCCESS.value in status) and any(
        error_status in status
        for error_status in {
            DQSTaskResultStatus.FAILED.value,
            DQSTaskResultStatus.TIMEOUT.value,
            DQSTaskResultStatus.SENT_TO_DLQ.value,
        }
    ):
        df["status"] = DQSReportStatus.PIPELINE_SUCCEEDED_WITH_ERRORS.value
        return df

    # Temporary status - DUMMY_SUCCESS. This is temporary until we finish all the DQ checks
    if (
        df["status"] == DQSTaskResultStatus.SUCCESS.value
    ).all() or DQSTaskResultStatus.DUMMY_SUCCESS.value in status:
        df["status"] = DQSReportStatus.PIPELINE_SUCCEEDED.value
        return df

    # The or condition is to mark the DQ Report as failed when there are no SUCCESS tasks and all tasks are either FAILED or TIMEOUT
    if (
        df["status"] == DQSTaskResultStatus.FAILED.value
    ).all() or DQSTaskResultStatus.SUCCESS.value not in status:
        df["status"] = DQSReportStatus.PIPELINE_FAILED.value
        return df
