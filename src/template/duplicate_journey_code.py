from multiprocessing.connection import Connection

from dqs_logger import logger
from common import Check
from enums import DQSTaskResultStatus
from dataframes import get_vj_duplicate_journey_code
from observation_results import ObservationResult
import hashlib
from dqs_exception import LambdaTimeOutError 
from time_out_handler import TimeOutHandler, get_timeout

def lambda_worker(event, check, pipe: Connection) -> None:
    status = DQSTaskResultStatus.SUCCESS.value
    try:
        observation = ObservationResult(check)
        logger.debug(f"Fetching the vj dataframe from db")
        df = get_vj_duplicate_journey_code(check)

        if not df.empty:
            df = df[df["journey_code"].notna() & (df["journey_code"] != "")]
            logger.debug(f"Looking in the Dataframes: {df.size}")
            df["hash"] = df.apply(create_df_row_hash, axis=1)

            duplicates = df[
                df.duplicated(subset=["line_ref", "journey_code", "hash","operating_on_working_days"], keep=False)
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

    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
        logger.exception(e)
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


def lambda_handler(event, context):
    try:
        # Get timeout from context reduced by 15 sec
        timeout = get_timeout(context)
        check = Check(event, __name__.split('.')[-1])
        check.validate_requested_check()
        timeout_handler = TimeOutHandler(event, check, timeout)
        return timeout_handler.run(lambda_worker)
    except LambdaTimeOutError:
        status = DQSTaskResultStatus.TIMEOUT.value 
        logger.info(f"Set status to {status}")
        check.set_status(status)
    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
        logger.exception(e)
        check.set_status(status)
