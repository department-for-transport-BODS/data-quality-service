from sqlalchemy import update
import pandas as pd
from dqs_logger import logger
from common import BodsDB
from contextlib import contextmanager


class DQReport:
    def __init__(self):
        self._db = BodsDB()
        self._table_name = self._db.classes.dqs_report

    def get_dq_reports_by_status(self, status: str) -> pd.DataFrame:
        df = pd.DataFrame()
        try:

            if status:
                query = self._db.session.query(self._table_name).filter(self._table_name.status == status)
                df = pd.read_sql_query(query.statement, self._db.session.bind)

        except Exception as e:
            logger.error(f"Failed to add observation for check = pipeline_monitor: {e}")
            raise e

        return df

    @contextmanager
    def update_dq_reports_status_using_ids(
        self, df_dq_reports: pd.DataFrame
    ) -> pd.DataFrame:

        try:
            if not df_dq_reports.empty:
                self._db.session.execute(
                    update(self._table_name), df_dq_reports.to_dict("records")
                )
                self._db.session.commit()
        except Exception as e:
            logger.error(f"Failed to add observation for check = pipeline_monitor: {e}")
            self._db.session.rollback()
            raise e
