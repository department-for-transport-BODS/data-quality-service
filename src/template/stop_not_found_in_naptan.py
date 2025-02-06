from dqs_logger import logger
from common import Check
from enums import DQSTaskResultStatus
from observation_results import ObservationResult
from dataframes import get_df_vehicle_journey, get_naptan_availablilty
from time_out_handler import TimeOutHandler, get_timeout
from dqs_exception import LambdaTimeOutError
import pandas as pd

def lambda_worker(event, check) -> None:

    status = DQSTaskResultStatus.SUCCESS.value
    try:
        observation = ObservationResult(check)
        df = get_df_vehicle_journey(check)
        logger.info(f"Looking in the Dataframes: {df.size}")
        if not df.empty:
            # Set of atco codes with case-insensitive
            atco_codes = set(df["atco_code"].str.lower())
            # List of atco codes from naptan stop point
            atco_codes_df = get_naptan_availablilty(check, atco_codes)
            atco_codes_df["atco_code_lower"] = atco_codes_df.atco_code.str.lower()
            atco_codes_df = atco_codes_df.drop("atco_code", axis=1)

            df["atco_code_lower"] = df.atco_code.str.lower()
            df = pd.merge(df, atco_codes_df, on="atco_code_lower", how="left")
            df.rename(columns={"common_name_x": "common_name"}, inplace=True)
            # Send the list to check with naptan stop point
            df = df[df["atco_code_exists"] == False]

            # df = df[df["naptan_stop_id"].isnull()]
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

    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
        logger.exception(e)
    finally:
        check.set_status(status)

    return


def lambda_handler(event, context):
    try:
        # Get timeout from context reduced by 15 sec
        timeout = get_timeout(context)
        check = Check(event, __name__.split('.')[-1])
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
        logger.exception(e)
        check.set_status(status)
