from os import environ
import logging
from common import Check


logger = logging.getLogger(__name__)
logger.setLevel(environ.get("LOG_LEVEL", "DEBUG"))


def lambda_handler(event, context):
    ### INITIATE A CHECK BASED ON INCOMING CHECK EVENT

    check = Check(event)

    ### VALIDATE THAT CHECK ID SENT TO LAMBDA EXISTS AND HAS A STATUS OF PENDING

    check.validate_requested_check()

    ### ADD AN OBSERVATION FOR YOUR CHECK

    # check.add_observation(
    #     vehicle_journey_id = 1,
    #     details = "Added Vehicle Journey ID"
    # )
    # check.add_observation(
    #     service_pattern_stop_id= 1,
    #     details = "Added Service Pattern Stop ID"
    # )

    ### WRITE ALL OBSERVATIONS TO DATABASE

    # check.write_observations()

    ### UPDATE CHECK STATUS FOLLOWING COMPLETION OF CHECKS

    check.set_status("SUCCESS")
    return
