from common import Check
from dqs_logger import logger
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound


class OrganisationTxcFileAttributes:
    """
    Class to handle the organisation_txcfileattributes table in database.

    Methods:
    validate_noc_code: Validate the NOC in the organisation_operatorcode table
    """

    def __init__(self, check: Check):
        self._check = check
        self.org_noc = None
        self._table = check.db.classes.organisation_txcfileattributes
        self._get_noc()

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
        except Exception as e:
            logger.error(
                f"Attempting to fetch details of organisation_txcfileattributes for id = {str(self._check.file_id)}",
                e,
            )
            raise e

    def validate_noc_code(self):
        """
        Method to validate the operator noc to the database
        """
        try:
            OperatorCode = self._check.db.classes.organisation_operatorcode
            row = (
                self._check.db.session.query(OperatorCode)
                .where(OperatorCode.noc == self.org_noc)
                .first()
            )

            if not row:
                return False
            return True
        except Exception as e:
            logger.error(
                f"Error in fetching the details from organisation_operatorcode noc = {str(self.org_noc)}",
                e,
            )
            raise e
