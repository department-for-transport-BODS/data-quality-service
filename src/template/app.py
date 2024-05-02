import psycopg2
from os import environ
from boto3 import client
import logging
from common import Check


logger = logging.getLogger(__name__)
logger.setLevel(environ.get("LOG_LEVEL", "DEBUG"))


def lambda_handler(event, context):
    check = Check(event)
    return(check.db.classes)
    # archive = db.classes.avl_cavldataarchive
    # first_archive_record = db.session.query(archive).first()
    # logger.debug(first_archive_record.__dict__)
