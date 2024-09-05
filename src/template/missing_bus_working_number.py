from dqs_logger import logger
from common import Check
from enums import DQSTaskResultStatus
from dataframes import get_df_missing_bus_working_number
from observation_results import ObservationResult
from time_out_handler import TimeOutHandler
from dqs_exception import LambdaTimeOutError


def lambda_handler(event, context):
    status = DQSTaskResultStatus.SUCCESS.value
    try:
        TimeOutHandler(context)
        check = Check(event)
        observation = ObservationResult(check)
        check.validate_requested_check()

        df = get_df_missing_bus_working_number(check)
        logger.info(f"Looking in the Dataframes: {df.size}")
        if not df.empty:
            logger.info("Iterating over rows to add observations")
            for row in df.itertuples():
                details = f"The ({row.start_time}) {row.direction} journey has not been assigned a bus working number (i.e. block number)."
                observation.add_observation(
                    details=details,
                    vehicle_journey_id=row.vehicle_journey_id,
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
