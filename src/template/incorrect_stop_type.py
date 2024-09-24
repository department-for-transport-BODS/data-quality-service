from common import Check
from enums import DQSTaskResultStatus
from dqs_logger import logger
from observation_results import ObservationResult
from dataframes import get_df_stop_type
from time_out_handler import TimeOutHandler
from dqs_exception import LambdaTimeOutError 
# List of allowed stop type for first stop
_ALLOWED_STOP_TYPES = ["BCT", "BCQ", "BCS", "BCE", "BST"]


def lambda_handler(event, context):

    status = DQSTaskResultStatus.SUCCESS.value
    try:
        check = Check(event)
        observation = ObservationResult(check)
        check.validate_requested_check()

        df = get_df_stop_type(check, _ALLOWED_STOP_TYPES)
        logger.info("Looking in the Dataframes")
        if not df.empty:
            logger.info("Iterating over rows to add observations")

            if len(_ALLOWED_STOP_TYPES) > 1:
                expected_stop_types = (
                    ", ".join(_ALLOWED_STOP_TYPES[:-1])
                    + " or "
                    + _ALLOWED_STOP_TYPES[-1]
                )
            else:
                expected_stop_types = _ALLOWED_STOP_TYPES[0]

            # Add the observation for check
            for row in df.itertuples():

                details = f"The {row.common_name} ({row.atco_code}) stop is registered as stop type {row.stop_type} with NaPTAN. Expected bus stop types are {expected_stop_types}."
                observation.add_observation(
                    details=details,
                    vehicle_journey_id=row.vehicle_journey_id,
                    service_pattern_stop_id=row.service_pattern_stop_id,
                )
                logger.info(
                    f"Adding observation:: {details}:: {row.vehicle_journey_id}:: {row.service_pattern_stop_id}"
                )

            logger.info("Observations added in memory")
            # Write the observations to database
            observation.write_observations()

    except LambdaTimeOutError as e:
        status = DQSTaskResultStatus.TIMEOUT.value
        logger.error(f"Check status timed out due to {e}")
    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
    finally:
        check.set_status(status)
        logger.info("Check status updated in DB")

    return
