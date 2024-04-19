import psycopg2
from os import environ
from boto3 import client
import logging
from common import BodsDB
logger = logging.getLogger(__name__)
logger.setLevel(environ.get("LOG_LEVEL", "DEBUG"))


def lambda_handler(event, context):
    db = BodsDB()
    archive = BodsDB.sqlalchemy_base.classes.avl_cavldataarchive
    first_archive_record = db.session.query(archive).first()
    logger.debug(first_archive_record.__dict__)
