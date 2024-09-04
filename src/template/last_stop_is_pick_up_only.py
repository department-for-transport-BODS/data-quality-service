from dqs_logger import logger
from common import Check
from enums import DQSTaskResultStatus
from observation_results import ObservationResult
from dataframes import get_df_vehicle_journey
from time_out_handler import TimeOutHandler
from dqs_exception import LambdaTimeOutError


# List of allowed activities for first stop
_ALLOWED_ACTIVITY_LAST_STOP = ["setDown", "setDownDriverRequest", "pickUpAndSetDown"]


def lambda_handler(event, context):
    status = DQSTaskResultStatus.SUCCESS.value
    try:
        TimeOutHandler(context)
        check = Check(event)
        observation = ObservationResult(check)
        check.validate_requested_check()

        df = get_df_vehicle_journey(check)
        logger.info(f"Looking in the Dataframes: {df.size}")
        if not df.empty:
            df = df.loc[df.groupby("vehicle_journey_id").auto_sequence_number.idxmax()]
            df = df[~df["activity"].isin(_ALLOWED_ACTIVITY_LAST_STOP)]

            logger.info("Iterating over rows to add observations")

            # Add the observation for check
            for row in df.itertuples():
                details = f"The last stop ({row.common_name}) on the {row.start_time} {row.direction} journey is incorrectly set to pick up passengers."
                observation.add_observation(
                    details=details,
                    vehicle_journey_id=row.vehicle_journey_id,
                    service_pattern_stop_id=row.service_pattern_stop_id,
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
