import pandas as pd
from dqs_logger import logger
from bods_db import BodsDB
from enums import DQSTaskResultStatus
from utils import get_uk_time
from models import DqsTaskresults as DqsTaskresultsModel


class DQTaskResults:
    def __init__(self):
        self._db = BodsDB()
        self._table_name = DqsTaskresultsModel

    def set_task_results_to_pending_status(self, revision_id) -> pd.DataFrame:
        df = pd.DataFrame()
        try:
            query = (
                self._db.session.query(self.service.txcfileattributes_id)
                .filter(
                    self.service.revision_id == revision_id,
                )
                .union()
            )
            txc_file_attributes_list = [
                txc_file_attributes.to_dict() for txc_file_attributes in query
            ]
            df = pd.read_sql_query(query.statement, self._db.session.bind)
        except Exception as e:
            logger.error(f"Failed to add observation for check = pipeline_monitor: {e}")
            raise e
        return txc_file_attributes_list

    def initialize_task_results(self, report_id: int, combinations: object) -> object:
        """
        Create a TaskResults object based on the given revision, TXCFileAttribute,
        and Check objects.
        """
        try:
            task_results_to_create = []
            for txc_file_attribute_id, check_id in combinations:
                if isinstance(txc_file_attribute_id, tuple):
                    txc_file_attribute_id = txc_file_attribute_id[0]

                task_results_to_create.append(
                    {
                        "created": get_uk_time(),
                        "modified": get_uk_time(),
                        "status": DQSTaskResultStatus.PENDING.value,
                        "message": "",
                        "checks_id": check_id,
                        "dataquality_report_id": report_id,
                        "transmodel_txcfileattributes_id": txc_file_attribute_id,
                    }
                )

            if task_results_to_create:
                self._db.session.bulk_insert_mappings(
                    self._table_name, task_results_to_create
                )
                self._db.session.commit()
            else:
                logger.warning("No task results to create")

        except Exception as e:
            logger.error(f"Failed to initialize task results: {e}")
            self._db.session.rollback()
            raise
