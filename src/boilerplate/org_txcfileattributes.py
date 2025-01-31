import pandas as pd
from dqs_logger import logger
from common import BodsDB

class TXCFileAttributes:
    def __init__(self):
        self._db = BodsDB()
        self._table_name = self._db.classes.organisation_txcfileattributes
        self.service = self._db.classes.transmodel_service

    def get_all_txc_file_attributes(self,revision_id) -> pd.DataFrame:
        df = pd.DataFrame()
        try:
            query = self._db.session.query(self.service.txcfileattributes_id).filter(
                self.service.revision_id == revision_id,
            ).union()
            txc_file_attributes_list = [txc_file_attributes.to_dict() for txc_file_attributes in query]
            # df = pd.read_sql_query(query.statement, self._db.session.bind)
        except Exception as e:
            logger.error(f"Failed to add observation for check = pipeline_monitor: {e}")
            raise e
        return txc_file_attributes_list



