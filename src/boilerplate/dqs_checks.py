import pandas as pd
from dqs_logger import logger
from common import BodsDB
from typing import List

class DQChecks:
    def __init__(self):
        self._db = BodsDB()
        self._table_name = self._db.classes.dqs_checks

    def get_all_checks(self) -> List:
        try:
            result = self._db.session.query(self._table_name).all()
        except Exception as e:
            logger.error(f"Field to retrieve checks : {e}")
            raise e
        return result

