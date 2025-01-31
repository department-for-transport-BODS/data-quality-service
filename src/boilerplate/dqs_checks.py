from sqlalchemy import update
import pandas as pd
from dqs_logger import logger
from common import BodsDB
from contextlib import contextmanager
from enums import ReportStatus, TaskResultsStatus


class DQChecks:
    def __init__(self):
        self._db = BodsDB()
        self._table_name = self._db.classes.dqs_checks

    def get_all_checks(self) -> pd.DataFrame:
        df = pd.DataFrame()
        try:
            query = self._db.session.query(self._table_name).all()
            # list of all the checks
            checks_list = [check.to_dict() for check in query]
            df = pd.read_sql_query(query.statement, self._db.session.bind)
        except Exception as e:
            logger.error(f"Failed to add observation for check = pipeline_monitor: {e}")
            raise e
        return checks_list

