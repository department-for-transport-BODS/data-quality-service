from sqlalchemy import update
import pandas as pd
from dqs_logger import logger
from common import Check
from contextlib import contextmanager


class DQReport:
    def __init__(self):
        self._check = Check()
        self._table_name = self._check.db.classes.dqs_report

    def get_dq_reports_by_status(self, status: str) -> pd.DataFrame:
        df = pd.DataFrame()
        try:

            if status:
                query = self._table_name.where(self._table_name.status == status)
                df = pd.read_sql_query(query, self._check.db.engine)

        except Exception as e:
            logger.error(f"Failed to add obervation for check = pipeline_monitor", e)
            raise e

        return df

    @contextmanager
    def update_dq_reports_status_using_ids(
        self, df_dq_reports: pd.DataFrame
    ) -> pd.DataFrame:

        try:

            if not df_dq_reports.empty:
                self._check.db.session.execute(
                    update(self._table_name), df_dq_reports.to_dict("records")
                )
                self._check.db.session.commit()
        except Exception as e:
            logger.error(f"Failed to add obervation for check = pipeline_monitor", e)
            self._check.db.session.rollback()
            raise e
