from os import environ
import pandas as pd

from src.boilerplate.enums import DQSTaskResultStatus, DQSReportStatus
from src.boilerplate.sqs import SQSClient


def get_generate_csv_queue_name() -> str:
    env = environ.get("ENV", "local")
    if env:
        return f"{env}-generate-csv"
    
    return None
    
    
def entries_generate_csv(df: pd.DataFrame) -> list:
    return df['id'].to_frame().to_dict('records')


def send_sqs_messages(df: pd.DataFrame):
    sqs = SQSClient()
    queue = sqs.get_sqs_queue(get_generate_csv_queue_name())
    sqs_entries = entries_generate_csv(df)
    sqs.send_messages(sqs_entries, queue)
    

def map_pipeline_status(df: pd.DataFrame) -> pd.DataFrame:
    status = set(df['status'])
    
    if DQSTaskResultStatus.PENDING in status:
        return pd.DataFrame()
         
    if ((DQSTaskResultStatus.SUCCESS in status) and (DQSTaskResultStatus.FAILED in status or DQSTaskResultStatus.TIMEOUT in status)):
        df['status'] = DQSReportStatus.PIPELINE_SUCCEEDED_WITH_ERRORS
        return df
    
    # Temporary status - DUMMY_SUCCESS. This is temporary until we finish all the DQ checks
    if (df['status'] == DQSTaskResultStatus.SUCCESS).all() or DQSTaskResultStatus.DUMMY_SUCCESS in status:
        df['status'] = DQSReportStatus.PIPELINE_SUCCEEDED
        return df
    
    # The or condition is to mark the DQ Report as failed when there are no SUCCESS tasks and all tasks are either FAILED or TIMEOUT
    if (df['status'] == DQSTaskResultStatus.FAILED).all() or DQSTaskResultStatus.SUCCESS not in status:
        df['status'] = DQSReportStatus.PIPELINE_FAILED
        return df
