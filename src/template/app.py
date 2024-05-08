import psycopg2
from os import environ
from boto3 import client
import logging
from common import Check


logger = logging.getLogger(__name__)
logger.setLevel(environ.get("LOG_LEVEL", "DEBUG"))


def lambda_handler(event, context):
    ### INITIATE A CHECK BASED ON INCOMING CHECK EVENT

    # check = Check(event)

    ### VALIDATE THAT CHECK ID SENT TO LAMBDA EXISTS AND HAS A STATUS OF PENDING

    # check.validate_requested_check()

    ### UPDATE CHECK STATUS FOLLOWING COMPLETION OF CHECKS

    # check.set_status("SUCCESS")
    return

