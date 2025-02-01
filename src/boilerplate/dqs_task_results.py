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
            task_results_to_create = []
            for txc_file_attribute_id, check_id in combinations:
                task_result = {
                    'status': TaskResultsStatus.PENDING.value,  # Status set to PENDING
                    'message': "",  # Empty message
                    'transmodel_txcfileattributes_id': txc_file_attribute_id,  # txcfileattributes_id
                    'checks_id': check_id,  # check_id
                    'dataquality_report_id': report_id  # report_id
                }
                task_results_to_create.append(task_result)  # Appending dictionary to list

            # Changed here: Using bulk_insert_mappings to insert a list of dictionaries
            self._db.session.bulk_insert_mappings(self._table_name, task_results_to_create)
            self._db.session.commit()
                # logger.info(f"the comps list: {txc_file_attribute_id}: {check.id}")   
                # task_results_to_create.append({
                #     "status": TaskResultsStatus.PENDING.value,
                #     "message": "",
                #     "checks_id": check.id,
                #     "dataquality_report_id": report_id,
                #     "transmodel_txcfileattributes_id": txc_file_attribute_id,
                # })

            # Execute the insert
            # self._db.session.execute(
            #     insert(self._table_name),  
            #     task_results_to_create
            # )
                        # Insert the task results using bulk_save_objects
            self._db.session.bulk_insert_mappings(self._table_name, task_results_to_create)
            self._db.session.commit()

        except Exception as e:
            logger.error(f"Failed to initialize task results: {e}")
            self._db.session.rollback()
            raise
