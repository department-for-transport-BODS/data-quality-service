from common import Check
from dqs_logger import logger
from observation_results import ObservationResult
from dataframes import get_df_stop_type
from boilerplate.enums import DQTaskResultStatus

# List of allowed stop type for first stop
_ALLOWED_STOP_TYPES = ["BCT", "BCQ", "BCS"]


def lambda_handler(event, context):
    try:
        check = Check(event)

        ### VALIDATE THAT CHECK ID SENT TO LAMBDA EXISTS AND HAS A STATUS OF PENDING
        if not check.validate_requested_check():
            logger.warning(f"Request is invalid")
            return

        df = get_df_stop_type(check, _ALLOWED_STOP_TYPES)
        logger.info("Looking in the Dataframes")
        if not df.empty:
            logger.info("Iterating over rows to add observations")

            if len(_ALLOWED_STOP_TYPES) > 1:
                expected_stop_types = (
                    ", ".join(_ALLOWED_STOP_TYPES[:-1]) + " or " + _ALLOWED_STOP_TYPES[-1]
                )
            else:
                expected_stop_types = _ALLOWED_STOP_TYPES[0]
            obs_result = ObservationResult(check)
            ### ADD AN OBSERVATION FOR YOUR CHECK
            for row in df.itertuples():

                details = f"The {row.common_name} ({row.atco_code}) stop is registered as stop type {row.stop_type} with NaPTAN. Expected bus stop types are {expected_stop_types}."
                obs_result.add_observation(
                    details=details,
                    vehicle_journey_id=row.vehicle_journey_id,
                    service_pattern_stop_id=row.service_pattern_stop_id,
                )
                logger.info(
                    f"Adding observation:: {details}:: {row.vehicle_journey_id}:: {row.service_pattern_stop_id}"
                )

            logger.info("Observations added in memory")
            ### WRITE ALL OBSERVATIONS TO DATABASE
            if len(obs_result.observations) > 0:
                obs_result.write_observations()
            logger.info("Observations written in DB")

        ### UPDATE CHECK STATUS FOLLOWING COMPLETION OF CHECKS
        check.set_status(DQTaskResultStatus.SUCCESS)
        logger.info("Check status updated in DB")
    except Exception as e:
        logger.error(e)
        check.set_status(DQTaskResultStatus.FAILED)
    return
