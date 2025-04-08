from common import Check
from dataframes import get_df_vehicle_journey


def lambda_handler(event, context):
    check = Check(event, "")

    get_df_vehicle_journey(check, refresh=True)
