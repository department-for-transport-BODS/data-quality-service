from dqs_logger import logger
from common import Check
from enums import DQSTaskResultStatus
from observation_results import ObservationResult
from dataframes import get_df_vehicle_journey


# List of allowed activities for first stop
_ALLOWED_ACTIVITY_LAST_STOP = ["setDown", "setDownDriverRequest"]


def lambda_handler(event, context):

    status = DQSTaskResultStatus.SUCCESS
    try:

        check = Check(event)
        observation = ObservationResult(check)
        check.validate_requested_check()

        df = get_df_vehicle_journey(check)
        logger.info(f"Looking in the Dataframes: {df.size}")
        if not df.empty:
            df = df.loc[df.groupby("vehicle_journey_id").sequence_number.idxmax()]
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
            if len(observation.observations) > 0:
                observation.write_observations()
                logger.info("Observations written in DB")

        logger.info("Check status updated in DB")
    except Exception as e:
        status = DQSTaskResultStatus.FAILED
        logger.error(f"Check status failed due to {e}")
    finally:
        check.set_status(status)

    return
