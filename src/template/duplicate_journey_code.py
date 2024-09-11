from dqs_logger import logger
from common import Check
from enums import DQSTaskResultStatus
from dataframes import get_vj_duplicate_journey_code
from observation_results import ObservationResult
import hashlib
from time_out_handler import TimeOutHandler
from dqs_exception import LambdaTimeOutError 

def lambda_handler(event, context):
    status = DQSTaskResultStatus.SUCCESS.value
    try:
        TimeOutHandler(context)
        check = Check(event)
        observation = ObservationResult(check)
        check.validate_requested_check()

        logger.debug(f"Fetching the vj dataframe from db")
        df = get_vj_duplicate_journey_code(check)

        logger.debug(f"Looking in the Dataframes: {df.size}")
        if not df.empty:
            df["hash"] = df.apply(create_df_row_hash, axis=1)

            duplicates = df[
                df.duplicated(subset=["line_ref", "journey_code", "hash"], keep=False)
            ]
            if not duplicates.empty:
                logger.debug(f"Found duplicate in the Dataframes: {duplicates.size}")
                for row in duplicates.itertuples():
                    details = f"The Journey Code ({row.journey_code}) is found in more than one vehicle journey."
                    observation.add_observation(
                        details=details,
                        vehicle_journey_id=row.vehicle_journey_id,
                        service_pattern_stop_id=row.service_pattern_stop_id,
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


def create_df_row_hash(row):
    return hashlib.md5(
        str(
            sorted(
                list(row["non_operating_date"])
                + list(row["operating_date"])
                + list(row["day_of_week"])
                + list(row["serviced_organisation_id"])
            )
        ).encode("utf-8")
    ).hexdigest()
