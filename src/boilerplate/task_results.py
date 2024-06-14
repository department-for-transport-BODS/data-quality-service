import pandas as pd
from dqs_logger import logger
from common import Check
from typing import List
from enums import DQSTaskResultStatus
from contextlib import contextmanager


class TaskResult:

    def __init__(self, check: Check, dq_report_ids: List) -> None:
        self._check = check
        self._report_ids = dq_report_ids
        self._table_name = self._check.db.classes.dqs_taskresults
        pass

    def get_task_results_df(self) -> pd.DataFrame:

        df = pd.DataFrame()
        try:

            if self._report_ids:
                query = self._table_name.where(
                    self._table_name.dataquality_report_id.in_(self._report_ids)
                )
            df = pd.read_sql_query(query, self._check.db.engine)

        except Exception as e:
            logger.error(
                f"Failed to fetch task results for check = pipeline_monitor", e
            )
            raise e

        return df

    @contextmanager
    def update_task_results_status_using_ids(self, status: str, check_id: str):
        try:
            if self._report_ids:

                update_task_results = (
                    self.db.session.query(self._table_name)
                    .filter(
                        self._table_name.dataquality_report_id.in_(self._report_ids)
                    )
                    .filter(self._table_name.status == DQSTaskResultStatus.PENDING)
                )
                for record in update_task_results:
                    record.status = status
                self.db.session.commit()
        except Exception as e:
            logger.error(
                f"Failed to update task result status for check = pipeline_monitor", e
            )
            self.db.session.rollback()
            raise e
