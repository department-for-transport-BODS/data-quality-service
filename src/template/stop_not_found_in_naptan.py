from common import Check
from observation_results import ObservationResult
from dataframes import get_df_vehicle_journey
from dqs_logger import logger
from boilerplate.enums import DQTaskResultStatus


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
            df = df[df["naptan_stop_id"].isnull()]
            df = df.loc[df.groupby("vehicle_journey_id").sequence_number.idxmax()]

            logger.info("Iterating over rows to add observations")

            ### ADD AN OBSERVATION FOR YOUR CHECK
            for row in df.itertuples():
                details = f"The {row.common_name} ({row.atco_code}) stop is not registered with NaPTAN. Please check the ATCO code is correct or contact your local authority to register this stop with NaPTAN."
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
