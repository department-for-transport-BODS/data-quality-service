from common import Check
from observation_results import ObservationResult
from dataframes import get_df_vehicle_journey
from dqs_logger import logger
from boilerplate.enums import DQTaskResultStatus


# List of allowed activities for first stop
_ALLOWED_ACTIVITY_LAST_STOP = ["setDown", "setDownDriverRequest"]


def lambda_handler(event, context):
    try:
        check = Check(event)
        observation = ObservationResult(check)

        ### VALIDATE THAT CHECK ID SENT TO LAMBDA EXISTS AND HAS A STATUS OF PENDING
        if not check.validate_requested_check():
            logger.warning(f"Request is invalid: {check}")
            return

        df = get_df_vehicle_journey(check)
        logger.info(f"Looking in the Dataframes: {df.size}")
        if not df.empty:
            df = df.loc[df.groupby("vehicle_journey_id").sequence_number.idxmax()]
            df = df[~df["activity"].isin(_ALLOWED_ACTIVITY_LAST_STOP)]

            logger.info("Iterating over rows to add observations")

            ### ADD AN OBSERVATION FOR YOUR CHECK
            for row in df.itertuples():
                details = f"The last stop ({row.common_name}) on the {row.start_time} {row.direction} journey is incorrectly set to pick up passengers."
                observation.add_observation(
                    details=details,
                    vehicle_journey_id=row.vehicle_journey_id,
                    service_pattern_stop_id=row.service_pattern_stop_id,
                )

            logger.info("Observations added in memory")
            ### WRITE ALL OBSERVATIONS TO DATABASE
            if len(observation.observations) > 0:
                observation.write_observations()
                logger.info("Observations written in DB")

        ### UPDATE CHECK STATUS FOLLOWING COMPLETION OF CHECKS
        check.set_status(DQTaskResultStatus.SUCCESS)
        logger.info("Check status updated in DB")
    except Exception as e:
        logger.error(f"Error: {e}")
        check.set_status(DQTaskResultStatus.FAILED)

    return
