import pandas as pd
from dqs_logger import logger
from common import BodsDB
from sqlalchemy import insert
from enums import TaskResultsStatus
class DQTaskResults:
    def __init__(self):
        self._db = BodsDB()
        self._table_name = self._db.classes.dqs_taskresults

    def set_task_results_to_pending_status(self,revision_id) -> pd.DataFrame:
        df = pd.DataFrame()
        try:
            query = self._db.session.query(self.service.txcfileattributes_id).filter(
                self.service.revision_id == revision_id,
            ).union()
            txc_file_attributes_list = [txc_file_attributes.to_dict() for txc_file_attributes in query]
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
            task_results_to_create = []  # List to hold task results as dictionaries
            for txc_file_attribute_id, check_id in combinations:
                if isinstance(txc_file_attribute_id, tuple):
                    txc_file_attribute_id = txc_file_attribute_id[0]
                logger.info(f"the comps list: {txc_file_attribute_id}: {check_id}")
                task_results_to_create.append({
                    "status": TaskResultsStatus.PENDING.value,
                    "message": "",  # Empty message
                    "checks_id": check_id,  # Use check_id from the combination tuple
                    "dataquality_report_id": report_id,  # report_id
                    "transmodel_txcfileattributes_id": txc_file_attribute_id,  # txc_file_attribute_id
                })

            # Use bulk_insert_mappings for better performance
            if task_results_to_create:
                self._db.session.bulk_insert_mappings(self._table_name, task_results_to_create)
                self._db.session.commit()  # Commit the transaction
            else:
                logger.warning("No task results to create!")

        except Exception as e:
            logger.error(f"Failed to initialize task results: {e}")
            self._db.session.rollback()
            raise
