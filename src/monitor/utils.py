import pandas as pd

from src.boilerplate.enums import DQ_Report_Status, DQ_Task_Result_Status


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
    