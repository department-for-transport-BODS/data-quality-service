from dqs_logger import logger
from common import Check
import pandas as pd
import numpy as np
from enums import DQSTaskResultStatus
from dataframes import get_df_vehicle_journey
from observation_results import ObservationResult
from time_out_handler import TimeOutHandler, get_timeout
from dqs_exception import LambdaTimeOutError 


def lambda_worker(event, check):

    status = DQSTaskResultStatus.SUCCESS.value
    try:
        observation = ObservationResult(check)
        df = get_df_vehicle_journey(check)
        df['vehicle_journey_code'] = df['vehicle_journey_code'].replace("", np.nan)
        logger.info(f"Looking in the Dataframes: {df.size}")
        if not df.empty:
            null_journey_codes = df[df['vehicle_journey_code'].isnull()]['vehicle_journey_id'].unique()
            df = df[df['vehicle_journey_id'].isin(null_journey_codes)]
            logger.info("Iterating over rows to add observations")
            # Sort the dataframe with vehicle journey id and auto sequence number
            df = df.sort_values(
                ["vehicle_journey_id", "auto_sequence_number"], ascending=True
            )
            df = df.groupby("vehicle_journey_id").first().reset_index()
            for row in df.itertuples():
                details = f"The ({row.start_time}) {row.direction} journey is missing a journey code."
                observation.add_observation(
                    details=details,
                    vehicle_journey_id=row.vehicle_journey_id,
                    service_pattern_stop_id=row.service_pattern_stop_id,
                )

                logger.info("Observation added in memory")

            observation.write_observations()

    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
    finally:
        check.set_status(status)
        logger.info("Check status updated in DB")

    return

def lambda_handler(event, context):
    try:
        # Get timeout from context reduced by 15 sec
        timeout = get_timeout(context)
        check = Check(event)
        check.validate_requested_check()
        timeout_handler = TimeOutHandler(event, check, timeout)
        timeout_handler.run(lambda_worker)
    except LambdaTimeOutError:
        status = DQSTaskResultStatus.TIMEOUT.value 
        logger.info(f"Set status to {status}")
        check.set_status(status)
    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
        check.set_status(status)
