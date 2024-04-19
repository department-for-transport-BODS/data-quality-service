from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import geoalchemy2
from os import environ
from boto3 import client
import logging
from json import loads
from pydantic import BaseModel

logger = logging.getLogger(__name__)
logger.setLevel(environ.get("LOG_LEVEL", "DEBUG"))


class EventPayload(BaseModel):
    txc_file_id: int
    check_id: int


class BodsDB:
    def __init__(self, lambda_event):
        self._lambda_event = lambda_event
        self._extract_test_details_from_event()
        self._initialise_database()

    def _extract_test_details_from_event(self):
        logger.debug("Event received:")
        logger.debug(self._lambda_event)
        try:
            event_payload = loads(self._lambda_event["Records"][0]["body"])
            logger.debug("Extracted Payload from event:")
            logger.debug(event_payload)
            logger.debug("Checking payload has required fields")
            check_details = EventPayload(**event_payload)
        except Exception as e:
            logger.error("Failed to extract a valid payload from the event")
            raise e
        logger.debug(
            f"Check_details found. TXC file ID={str(check_details.txc_file_id)}, check ID={str(check_details.check_id)}"
        )
        self.file_id = check_details.txc_file_id
        self.check_id = check_details.check_id

    def _initialise_database(self):
        logger.debug("Getting DB password from secrets manager")
        secrets_manager = client("secretsmanager")
        password_response = secrets_manager.get_secret_value(
            SecretId=environ.get("POSTGRES_PASSWORD"),
        )
        pg_pass = password_response["SecretString"]
        logger.debug("Got DB password")

        pg_host = environ.get("POSTGRES_HOST")
        pg_db = environ.get("POSTGRES_DB")
        pg_user = environ.get("POSTGRES_USER")
        pg_port = environ.get("POSTGRES_PORT")
        logger.debug(
            f"Connecting to DB with connection string postgresql+psycopg2://{pg_user}:<password obfuscated>@{pg_host}:{pg_port}/{pg_db}"
        )
        self.sqlalchemy_base = automap_base()
        sqlalchemy_engine = create_engine(
            f"postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
        )
        logger.debug("Preparing SQLALchemy base")
        self.sqlalchemy_base.prepare(autoload_with=sqlalchemy_engine)
        logger.debug("Initiating DB session")
        self.session = Session(sqlalchemy_engine)
        logger.debug("Connected to DB")
