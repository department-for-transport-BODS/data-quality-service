from dqs_logger import logger
from common import Check
from enums import DQSTaskResultStatus
from dataframes import get_vj_duplicate_journey_code
from observation_results import ObservationResult
import pandas as pd
import hashlib


def lambda_handler(event, context):
    status = DQSTaskResultStatus.SUCCESS.value
    try:
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", None)

        check = Check(event)
        observation = ObservationResult(check)
        check.validate_requested_check()

        df = get_vj_duplicate_journey_code(check)
        logger.info(f"Looking in the Dataframes: {df.size}")

        df["hash"] = df.apply(create_df_row_hash, axis=1)

        duplicates = df[
            df.duplicated(
                subset=["line_ref", "journey_code", "hash"], keep=False
            )
        ]
        logger.info(f"Found duplicate in the Dataframes: {duplicates.size}")
        for row in duplicates.itertuples():
            details = f"The Journey Code ({row.journey_code}) is found in more than one vehicle journey."
            observation.add_observation(
                details=details,
                vehicle_journey_id=row.vehicle_journey_id,
                service_pattern_stop_id=row.service_pattern_stop_id,
            )

            logger.info("Observation added in memory")
        # Write the observations to database
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


def create_df_row_hash(row):
    return hashlib.md5(
        str(
            sorted(
                row[["non_operating_date"]]
                + row[["operating_date"]]
                + row[["day_of_week"]]
                + row[["serviced_organisation_id"]]
            )
        ).encode("utf-8")
    ).hexdigest()
