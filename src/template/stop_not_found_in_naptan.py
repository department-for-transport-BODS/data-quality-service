from dqs_logger import logger
from common import Check
from enums import DQSTaskResultStatus
from observation_results import ObservationResult
from dataframes import get_df_vehicle_journey
from time_out_handler import TimeOutHandler
from dqs_exception import LambdaTimeOutError 

def lambda_handler(event, context):

    status = DQSTaskResultStatus.SUCCESS.value
    try:

        check = Check(event)
        TimeOutHandler(context)
        observation = ObservationResult(check)
        check.validate_requested_check()

        df = get_df_vehicle_journey(check)
        logger.info(f"Looking in the Dataframes: {df.size}")
        if not df.empty:
            df = df[df["naptan_stop_id"].isnull()]
            logger.info("Iterating over rows to add observations")

            # Add the observation for check
            for row in df.itertuples():
                details = f"The {row.common_name} ({row.atco_code}) stop is not registered with NaPTAN. Please check the ATCO code is correct or contact your local authority to register this stop with NaPTAN."
                observation.add_observation(
                    details=details,
                    vehicle_journey_id=row.vehicle_journey_id,
                    service_pattern_stop_id=row.service_pattern_stop_id,
                )

            logger.info("Observations added in memory")
            # Write the observations to database
            observation.write_observations()
            logger.info("Observations written in DB")
    
    except LambdaTimeOutError as e:
        status = DQSTaskResultStatus.TIMEOUT.value
        logger.error(f"Check status timed out due to {e}")

        logger.info("Check status updated in DB")
    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
    finally:
        check.set_status(status)

    return
