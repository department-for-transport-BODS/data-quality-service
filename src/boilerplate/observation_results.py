from common import Check
from dqs_logger import logger
from models import DqsObservationresults


class ObservationResult:
    """
    Class to handle the observation result table in database.

    Attributes:
    observations: list

    Properties:
    task_results: dqs_taskresults table

    Methods:
    add_observation: Add an observation to the check
    write_observations: Write the observations to the database
    """

    def __init__(self, check: Check):
        self._check = check
        self.observations = []
        self._table = DqsObservationresults

    def add_observation(
        self,
        details=None,
        vehicle_journey_id=None,
        service_pattern_stop_id=None,
        serviced_organisation_vehicle_journey_id=None,
    ):
        """
        Method to add an observation to the check

        Args:
        details: str, optional
        vehicle_journey_id: int, optional
        service_pattern_stop_id: int, optional
        serviced_organisation_id: int, optional
        """
        try:
            self._check.validate_requested_check()
            logger.debug(
                f"Attempting to add observation for check_id = {str(self._check.check_id)}"
            )
            observation = self._table(
                details=details,
                taskresults_id=self._check.result_id,
                vehicle_journey_id=vehicle_journey_id,
                service_pattern_stop_id=service_pattern_stop_id,
                serviced_organisation_vehicle_journey_id=serviced_organisation_vehicle_journey_id,
            )
            self._check.db.session.add(observation)
            self.observations.append(observation)
        except Exception as e:
            logger.error(
                f"Failed to add observation for check_id = {str(self._check.check_id)}",
                e,
            )
            raise e

    def write_observations(self):
        """
        Method to write the added observations to the database
        """
        try:
            if len(self.observations) < 1:
                logger.info(
                    f"No observations to write for check_id = {str(self._check.check_id)}"
                )
                return
            logger.debug(
                f"Attempting to add {str(len(self.observations))} observation(s) for check_id = {str(self._check.check_id)}"
            )
            self._check.db.session.flush()
            self._check.db.session.commit()
            logger.info("Observations written in DB")
        except Exception as e:
            logger.error(
                f"Attempting to add observation for check_id = {str(self._check.check_id)}",
                e,
            )
            raise e
