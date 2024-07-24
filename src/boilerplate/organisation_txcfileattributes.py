from common import Check
from dqs_logger import logger
from sqlalchemy import and_


class OrganisationTxcFileAttributes:
    """
    Class to handle the organisation_txcfileattributes table in database.

    Methods:
    validate_noc_code: Validate the NOC in the organisation_operatorcode table
    """

    def __init__(self, check: Check):
        self._check = check
        self.org_noc = None
        self.revision_id = None
        self.dataset_id = None
        self.organisation_id = None
        self._table = check.db.classes.organisation_txcfileattributes
        self._get_noc()
        self._get_organisation_dataset()
        self._get_organisation_id()


    def _get_noc(self):
        """
        Method to get the noc
        """
        try:
            result = (
                self._check.db.session.query(self._table)
                .where(self._table.id == self._check.file_id)
                .first()
            )
            self.org_noc = result.national_operator_code
            self.revision_id = result.revision_id
        except Exception as e:
            logger.error(
                f"Attempting to fetch details of organisation_txcfileattributes for id = {str(self._check.file_id)}",
                e,
            )
            raise e
    
    def _get_organisation_dataset(self):
        """
        Method to get the organisation dataset objects
        """
        OrganisationDatasetRevision = self._check.db.classes.organisation_datasetrevision
        try:
            result = (
                self._check.db.session.query(OrganisationDatasetRevision)
                .where(OrganisationDatasetRevision.revision_id == self.revision_id)
                .first()
            )
            self.dataset_id = result.dataset_id
        except Exception as e:
            logger.error(
                f"Attempting to fetch details of organisation_dataset for id = {str(self._check.file_id)}",
                e,
            )
            raise e
    
    def _get_organisation_id(self):
        """
        Method to get the organisation dataset objects
        """
        OrganisationDataset = self._check.db.classes.organisation_dataset
        try:
            result = (
                self._check.db.session.query(OrganisationDataset)
                .where(OrganisationDataset.id == self.dataset_id)
                .first()
            )
            self.organisation_id = result.organisation_id
        except Exception as e:
            logger.error(
                f"Attempting to fetch details of organisation_dataset for id = {str(self._check.file_id)}",
                e,
            )
            raise e

    def validate_noc_code(self):
        """
        Method to validate the operator noc to the database
        """
        try:
            OperatorCode = self._check.db.classes.organisation_operatorcode
            row_operator_code = (
                self._check.db.session.query(OperatorCode)
                .filter(and_(OperatorCode.noc == self.org_noc, OperatorCode.organisation_id == self.organisation_id))
                .first()
            )
            if not row_operator_code:
                return False
            return True
        except Exception as e:
            logger.error(
                f"Error in fetching the details from organisation_operatorcode noc = {str(self.org_noc)}",
                e,
            )
            raise e
