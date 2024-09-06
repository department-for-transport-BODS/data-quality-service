from dqs_logger import logger
from common import Check
from enums import DQSTaskResultStatus
from dataframes import get_df_vehicle_journey
from observation_results import ObservationResult
import pandas as pd
from time_out_handler import TimeOutHandler
from dqs_exception import LambdaTimeOutError 
from datetime import timedelta

_ALLOWED_IS_TIMING_POINT = True


def filter_vehicle_journey(df: pd.DataFrame, observation: ObservationResult) -> bool:
    """
    Filter the service pattern stop whose departure time is having a
    gap of more than or equal to 15 mins.
    """

    df["departure_time_new"] = pd.to_datetime(df["departure_time"], format="%H:%M:%S")
    df["time_diff"] = df["departure_time_new"].diff()
    df["departure_time"] = df["departure_time"].apply(lambda x: x.strftime("%H:%M"))
    df = df.reset_index()

    for i in range(1, len(df)):
        if df.loc[i, "time_diff"] >= timedelta(minutes=15):

            prev_row = df.iloc[i - 1]
            curr_row = df.iloc[i]
            details = (
                f"The link between the {prev_row['departure_time']} {prev_row['common_name']} ({prev_row['atco_code']}) and"
                f" {curr_row['departure_time']} {curr_row['common_name']} ({curr_row['atco_code']}) timing point stop is"
                " more than 15 minutes apart. The Traffic Comissioner recommends services to have timing points"
                " no more than 15 minutes apart."
            )
            observation.add_observation(
                details=details,
                vehicle_journey_id=int(prev_row.vehicle_journey_id),
                service_pattern_stop_id=int(prev_row.service_pattern_stop_id),
            )

            logger.info("Observation added in memory")


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
            # Filter the timing point stops
            df = df[df["is_timing_point"] == _ALLOWED_IS_TIMING_POINT]
            df = df.sort_values(by="auto_sequence_number")
            df.groupby("vehicle_journey_id").apply(filter_vehicle_journey, observation)

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
