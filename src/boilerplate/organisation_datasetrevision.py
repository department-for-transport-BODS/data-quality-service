import pandas as pd
from dqs_logger import logger
from bods_db import BodsDB
from models import OrganisationDatasetrevision


class Revision:
    def __init__(self):
        self._db = BodsDB()
        self._table_name = OrganisationDatasetrevision

    def get_revision(self, revision_id) -> pd.DataFrame:
        try:
            result = (
                self._db.session.query(self._table_name)
                .filter(
                    self._table_name.id == revision_id,
                )
                .first()
            )
            logger.info(f"Rfevision results: {result}")
            return result
        except Exception as e:
            logger.error(f"Getting Revision objection failed due to: {e}")
            raise e
