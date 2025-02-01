import pandas as pd
from dqs_logger import logger
from common import BodsDB
from typing import List

class DQChecks:
    def __init__(self):
        self._db = BodsDB()
        self._table_name = self._db.classes.dqs_checks

    def get_all_check_ids(self) -> List[int]:
        try:
            return [check_id for check_id, in self._db.session.query(self._table_name.id).all()]
        except Exception as e:
            logger.error(f"Failed to retrieve check ids: {e}")
            raise

