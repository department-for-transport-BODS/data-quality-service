from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import geoalchemy2
from os import environ
from boto3 import client
import logging
logger = logging.getLogger(__name__)
logger.setLevel(environ.get("LOG_LEVEL", "DEBUG"))

class BodsDB:
    def __init__(self):
        logger.debug('Getting DB password from secrets manager')
        secrets_manager = client('secretsmanager')
        password_response = secrets_manager.get_secret_value(
            SecretId=environ.get('POSTGRES_PASSWORD'),
        )
        pg_pass = password_response['SecretString']
        logger.debug('Got DB password')

        pg_host = environ.get('POSTGRES_HOST')
        pg_db = environ.get('POSTGRES_DB')
        pg_user = environ.get('POSTGRES_USER')
        pg_port = environ.get('POSTGRES_PORT')
        logger.debug(f'Connecting to DB with connection string postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
        self.sqlalchemy_base = automap_base()
        sqlalchemy_engine = create_engine(f"postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}")
        logger.debug('Preparing SQLALchemy base')
        self.sqlalchemy_base.prepare(autoload_with=sqlalchemy_engine)
        logger.debug('Initiating DB session')
        self.session = Session(sqlalchemy_engine)
        logger.debug('Connected to DB')