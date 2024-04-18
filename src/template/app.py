import psycopg2
from os import environ
from boto3 import client
import logging
from common import test
logger = logging.getLogger(__name__)
logger.setLevel(environ.get("LOG_LEVEL", "DEBUG"))


def lambda_handler(event, context):
    logger.debug('Getting password from secrets manager')
    secrets_manager = client('secretsmanager')
    response = secrets_manager.get_secret_value(
        SecretId=environ.get('POSTGRES_PASSWORD'),

    )
    pg_pass = response['SecretString']
    logger.debug('Got password')

    logger.debug('Connecting to DB')
    pg_host = environ.get('POSTGRES_HOST')
    pg_db = environ.get('POSTGRES_DB')
    pg_user = environ.get('POSTGRES_USER')
    postgres_connection = psycopg2.connect(f"dbname='{pg_db}' user='{pg_user}' host='{pg_host}' password='{pg_pass}'")
    logger.debug('Connected to DB')

    logger.debug('Getting sample data')
    with postgres_connection.cursor() as curs:
        curs.execute('select * from data_quality_dataqualityreport limit 1')
        logger.debug(curs.fetchone())
    logger.debug('Got sample data')

    postgres_connection.close()
    logger.debug(f"Layer returned {test()}")
