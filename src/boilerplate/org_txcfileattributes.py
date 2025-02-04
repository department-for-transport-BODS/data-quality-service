from dqs_logger import logger
from common import BodsDB
from typing import List

class TXCFileAttributes:
    def __init__(self):
        self._db = BodsDB()
        self._table_name = self._db.classes.organisation_txcfileattributes
        self.service = self._db.classes.transmodel_service

    def get_all_txc_file_attributes(self, revision_id) -> List:
        try:
            result = self._db.session.query(self.service.txcfileattributes_id).filter(
                self.service.revision_id == revision_id
            ).distinct().all()
            logger.info(f"txc_file query result: {result}")

            return [txc_file_attribute for txc_file_attribute, in result]

        except Exception as e:
            logger.error(f"Failed to retrieve txc_file ids: {e}")
            raise e
