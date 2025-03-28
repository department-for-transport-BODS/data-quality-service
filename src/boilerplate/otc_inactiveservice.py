from common import Check
from dqs_logger import logger
from sqlalchemy import and_
from datetime import datetime
from models import OtcInactiveservice as OtcInactiveServiceModel


class OtcInactiveService:
    """
    Class to handle the otc_inactiveservice table in database.

    Methods:
    is_service_exists: Is the service exists in otc_inactiveservice table for service with gte today's date
    """

    def __init__(self, check: Check):
        self._check = check
        self._table = OtcInactiveServiceModel

    def is_service_exists(self, registration_number: str):
        """
        Method to check whether the service exists in otc_inactiveservice
        table for service with greater than today's date
        """
        curr_date = datetime.now().date()
        try:
            result = (
                self._check.db.session.query(self._table.registration_number)
                .where(
                    (
                        (self._table.registration_number == registration_number)
                        or (
                            self._table.registration_number
                            == registration_number.replace(":", "/")
                        )
                    )
                    & (self._table.effective_date >= curr_date)
                )
                .first()
            )

            if result:
                return True
            return False

        except Exception as e:
            logger.error(
                (
                    f"Attempting to fetch details of otc_inactiveservice for registration number = {str(registration_number)} and effective date > {curr_date}"
                ),
                e,
            )
            raise e
