from dqs_logger import logger
from common import Check
from enums import DQSTaskResultStatus
from observation_results import ObservationResult
from time_out_handler import TimeOutHandler
from dqs_exception import LambdaTimeOutError
from dataframes import get_df_serviced_organisation
from datetime import datetime
from time_out_handler import TimeOutHandler, get_timeout


def lambda_worker(event, check):
    status = DQSTaskResultStatus.SUCCESS.value

    try:
        observation = ObservationResult(check)
        df = get_df_serviced_organisation(check)
        if not df.empty:

            # Sort the values by the end date
            df = df.sort_values(by=["serviced_organisation_end_date"])

            # For every vehicle journey id, find the last end date
            df = df.loc[
                df.groupby(by="serviced_organisation_id")[
                    "serviced_organisation_end_date"
                ].idxmax()
            ]
            # Reset index
            df = df.reset_index()

            # Compare the today date for the serviced organisation working day
            today_date = datetime.now().date()
            df = df[df["serviced_organisation_end_date"] < today_date]

            for row in df.itertuples():
                end_date = datetime.strftime(
                    row.serviced_organisation_end_date, "%d/%m/%Y"
                )
                details = (
                    f"The Working Days for Serviced Organisation {row.serviced_organisation_name} "
                    f"({row.serviced_organisation_code}) has expired on {end_date}. "
                    "Please update the dates for this Serviced Organisation."
                )
                observation.add_observation(
                    details=details, vehicle_journey_id=row.vehicle_journey_id
                )
                logger.info("Observation added in memory")

            # Write the observations to database
            observation.write_observations()

        logger.info("Check status updated in DB")

    except LambdaTimeOutError as e:
        status = DQSTaskResultStatus.TIMEOUT.value
        logger.error(f"Check status timed out due to {e}")
    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
    finally:
        check.set_status(status)
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
