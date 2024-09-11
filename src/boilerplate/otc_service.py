from common import Check
from dqs_logger import logger


class OtcService:
    """
    Class to handle the otc_service table in database.

    Methods:
    is_service_exists: Is the service exists in otc_service table with filter on registration number
    """

    def __init__(self, check: Check):
        self._check = check
        self._table = check.db.classes.otc_service

    def is_service_exists(self, registration_number: str):
        """
        Method to get the details by registration number
        """
        try:
            result = (
                self._check.db.session.query(self._table.registration_number)
                .where(
                    (self._table.registration_number == registration_number)
                    or (
                        self._table.registration_number
                        == registration_number.replace(":", "/")
                    )
                )
                .first()
            )

            if result:
                return True
            return False

        except Exception as e:
            logger.error(
                f"Attempting to fetch details of otc_service for registration number = {str(registration_number)}",
                e,
            )
            raise e
