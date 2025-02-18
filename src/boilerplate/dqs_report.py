from typing import List
from sqlalchemy import update
import pandas as pd
from dqs_logger import logger
from common import BodsDB
from contextlib import contextmanager
from enums import DQSReportStatus
from utils import get_uk_time

class DQReport:
    def __init__(self):
        self._db = BodsDB()
        self._table_name = self._db.classes.dqs_report

    @property
    def db(self):
        return self._db

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

    def get_dq_report_by_revision_id(self, revision_id: int, status) -> pd.DataFrame:
        df = pd.DataFrame()
        try:
            if revision_id:
                query = self._db.session.query(self._table_name).filter(
                    self._table_name.revision_id == revision_id).filter(
                        self._table_name.status == status)
                df = pd.read_sql_query(query.statement, self._db.session.bind)
        except Exception as e:
            logger.error(f"Failed to add observation for check = pipeline_monitor: {e}")
            raise e
        return df

    
    def initialise_dqs_report(self, revision_id: int) -> int:
        """
        Create a new Report instance with the provided data and save it to the database.
        """
        try:
            existing_report = self._db.session.query(self._table_name).filter(self._table_name.revision_id == revision_id).first()
            if existing_report:
                self._db.session.delete(existing_report)

            new_report = self._table_name(file_name="",created=get_uk_time(), revision_id=revision_id, status=DQSReportStatus.PIPELINE_PENDING.value)
            self._db.session.add(new_report)
            self._db.session.commit()
            report_id = new_report.id
            logger.info(f"Report object created with id: {report_id}")

            return report_id
        except Exception as e:
            logger.error(f"Failed to initialise DQS task: {e}")
            self._db.session.rollback()
            raise e

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
