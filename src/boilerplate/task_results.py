import pandas as pd
from dqs_logger import logger
from bods_db import BodsDB
from typing import List
from enums import DQSTaskResultStatus
from contextlib import contextmanager
from models import DqsTaskresults


class TaskResult:
    def __init__(self, dq_report_ids: List) -> None:
        self._db = BodsDB()
        self._report_ids = dq_report_ids
        self._table_name = DqsTaskresults

    def get_task_results_df(self) -> pd.DataFrame:
        df = pd.DataFrame()
        try:
            if self._report_ids:
                query = self._db.session.query(self._table_name).filter(
                    self._table_name.dataquality_report_id.in_(self._report_ids)
                )
                df = pd.read_sql_query(query.statement, self._db.session.bind)

        except Exception as e:
            logger.error(
                f"Failed to fetch task results for report id{self._report_ids}"
            )
            raise e

        return df

    def get_pending_task_results_df(self) -> pd.DataFrame:
        df = pd.DataFrame()
        try:
            if self._report_ids:
                query = self._db.session.query(self._table_name).filter(
                    self._table_name.dataquality_report_id.in_(self._report_ids)
                )
                df = pd.read_sql_query(query.statement, self._db.session.bind)

        except Exception as e:
            logger.error(
                f"Failed to fetch task results for check = pipeline_monitor: {e}"
            )
            raise e

        return df

    @contextmanager
    def update_task_results_status_using_ids(self, status: str):
        try:
            if self._report_ids:
                task_results = (
                    self._db.session.query(self._table_name)
                    .filter(
                        self._table_name.dataquality_report_id.in_(self._report_ids)
                    )
                    .filter(
                        self._table_name.status == DQSTaskResultStatus.PENDING.value
                    )
                )
                for record in task_results:
                    record.status = status
                self._db.session.commit()
        except Exception as e:
            logger.error(
                f"Failed to update task result status for check = pipeline_monitor: {e}"
            )
            self._db.session.rollback()
            raise e
