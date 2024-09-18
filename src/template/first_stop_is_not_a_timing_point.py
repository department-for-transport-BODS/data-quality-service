from dqs_logger import logger
from common import Check
from enums import DQSTaskResultStatus
from dataframes import get_df_vehicle_journey
from observation_results import ObservationResult
from time_out_handler import TimeOutHandler
from dqs_exception import LambdaTimeOutError 

_ALLOWED_IS_TIMING_POINT = True


def lambda_handler(event, context):

    status = DQSTaskResultStatus.SUCCESS.value
    try:
        check = Check(event)
        observation = ObservationResult(check)
        check.validate_requested_check()

        df = get_df_vehicle_journey(check)
        logger.info(f"Looking in the Dataframes: {df.size}")
        if not df.empty:
            df = df.loc[df.groupby("vehicle_journey_id").auto_sequence_number.idxmin()]
            df = df[~df["is_timing_point"] == _ALLOWED_IS_TIMING_POINT]
            logger.info("Iterating over rows to add observations")

            # Add the observation for check
            for row in df.itertuples():
                details = f"The first stop ({row.common_name}) on the {row.start_time} {row.direction} journey is not set as a timing point."
                observation.add_observation(
                    details=details,
                    vehicle_journey_id=row.vehicle_journey_id,
                    service_pattern_stop_id=row.service_pattern_stop_id,
                )

                logger.info("Observation added in memory")
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
