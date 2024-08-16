from dqs_logger import logger
from common import Check
import pandas as pd
import numpy as np
from enums import DQSTaskResultStatus
from dataframes import get_df_vehicle_journey
from observation_results import ObservationResult


def lambda_handler(event, context):

    status = DQSTaskResultStatus.SUCCESS.value
    try:
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        check = Check(event)
        observation = ObservationResult(check)
        check.validate_requested_check()

        df = get_df_vehicle_journey(check)
        df['vehicle_journey_code'] = df['vehicle_journey_code'].replace("", np.nan)
        logger.info(f"Looking in the Dataframes: {df.size}")
        if not df.empty:
                null_journey_codes = df[df['vehicle_journey_code'].isnull()]['vehicle_journey_id'].unique()
                df = df[df['vehicle_journey_id'].isin(null_journey_codes)]

                logger.info("Iterating over rows to add observations")
                for row in df.itertuples():
                    details = f"The ({row.start_time}) {row.direction} journey is missing a journey code."
                    observation.add_observation(
                        details=details,
                        vehicle_journey_id=row.vehicle_journey_id,
                        service_pattern_stop_id=row.service_pattern_stop_id,
                    )

                    logger.info("Observation added in memory")

                if len(observation.observations) > 0:
                    observation.write_observations()
                    logger.info("Observations written in DB")

        logger.info("Check status updated in DB")
    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
    finally:
        check.set_status(status)

    return
