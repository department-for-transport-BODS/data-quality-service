import os
import pandas as pd

from src.boilerplate.enums import DQ_Report_Status, DQ_Task_Result_Status
from src.boilerplate.sqs import SQSClient


def get_generate_csv_queue_name() -> str:
    env = os.environ["ENV"]
    repo = os.environ["REPOSITORY"]
    if env and repo:
        return f"{repo}-generate-csv-{env}"
    
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
    
    if DQ_Task_Result_Status.PENDING in status:
        return pd.DataFrame()
         
    if ((DQ_Task_Result_Status.SUCCESS in status) and (DQ_Task_Result_Status.FAILED in  status or DQ_Task_Result_Status.TIMEOUT in  status)):
        df['status'] = DQ_Report_Status.PIPELINE_SUCCEEDED_WITH_ERRORS
        return df
    
    if (df['status'] == DQ_Task_Result_Status.SUCCESS).all():
        df['status'] = DQ_Report_Status.PIPELINE_SUCCEEDED
        return df
    
    # The or condition is to mark the DQ Report as failed when there are no SUCCESS tasks and all tasks are either FAILED or TIMEOUT
    if (df['status'] == DQ_Task_Result_Status.FAILED).all() or DQ_Task_Result_Status.SUCCESS not in status:
        df['status'] = DQ_Report_Status.PIPELINE_FAILED
        return df
    