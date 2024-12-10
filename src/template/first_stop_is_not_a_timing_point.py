from multiprocessing.queues import Queue

from dqs_logger import logger
from common import Check
from enums import DQSTaskResultStatus
from dataframes import get_df_vehicle_journey
from observation_results import ObservationResult
from pandas import DataFrame
from time_out_handler import TimeOutHandler, get_timeout
from dqs_exception import LambdaTimeOutError 

_ALLOWED_IS_TIMING_POINT = True


def lambda_worker(event, check, queue: Queue) -> None:

    status = DQSTaskResultStatus.SUCCESS.value
    try:
        observation = ObservationResult(check)
        df = get_df_vehicle_journey(check)
        # Make sure the DF and event pass downstream
        queue.put(dict(**event,previous_result=df.to_dict()))

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
    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
        logger.exception(e)
    finally:
        check.set_status(status)
        logger.info("Check status updated in DB")

def lambda_handler(event, context):
    try:
        # Get timeout from context reduced by 15 sec
        timeout = get_timeout(context)
        check = Check(event, context)
        check.validate_requested_check()
        timeout_handler = TimeOutHandler(event, check, timeout)
        return timeout_handler.run(lambda_worker)
    except LambdaTimeOutError:
        status = DQSTaskResultStatus.TIMEOUT.value 
        logger.info(f"Set status to {status}")
        check.set_status(status)
    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
        check.set_status(status)