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
    file_id: int
    check_id: int
    result_id: int



class Check:
    def __init__(self, lambda_event):
        self._lambda_event = lambda_event
        self._file_id = None
        self._check_id = None
        self._db = None
        self._task_results_table = None
        self._observation_results_table = None
        self._task_result_id = None

    @property
    def db(self):
        if self._db is None:
            self._db = BodsDB()
        return self._db

    @property
    def file_id(self):
        if self._file_id is None:
            self._extract_test_details_from_event()
        return self._file_id

    @property
    def check_id(self):
        if self._check_id is None:
            self._extract_test_details_from_event()
        return self._check_id
    
    @property
    def task_results(self):
        if self._task_results_table is None:
            self._task_results_table = self.db.classes.data_quality_taskresult
        return self._task_results_table
    
    @property
    def observation_results(self):
        if self._task_results_table is None:
            self._task_results_table = self.db.classes.data_quality_observationresults
        return self._observation_results_table
    
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
            f"Check_details found. TXC file ID={str(check_details.file_id)}, check ID={str(check_details.check_id)}"
        )
        self._file_id = check_details.file_id
        self._check_id = check_details.check_id

    @property
    def task_result_id(self):
        if self._task_result_id is None:
            try:
                logger.debug(f'Getting task results id for file id = {self.file_id}, check id = {self.check_id}')
                task_result_ids = self.db.session.query(self.task_results).filter(
                    self.task_results.transmodel_txcfileattributes_id == self.file_id, 
                    self.task_results.checks_id == self.check_id
                ).all()
                if len(task_result_ids) == 1:
                    self._task_result_id =  task_result_ids[0].id
                else:
                    logger.error(
                        f'Invalid Task Result - no record waiting for file id {self.file_id} '
                        f'for check if {self.check_id}'
                    )
                    raise ValueError
            except Exception as e:
                logger.error(
                    f'Invalid Task Result - failed to get record for file id {self.file_id} '
                    f'for check if {self.check_id}'
                )
                raise e
        return self._task_result_id

class BodsDB:
    def __init__(self):
        self._session = None
        self._classes = None

    @property
    def session(self):
        if self._session is None:
            self._initialise_database()
        return self._session

    @property
    def classes(self):
        if self._classes is None:
            self._initialise_database()
        return self._classes

    def _initialise_database(self):
        connection_details = self._get_connection_details()
        logger.debug(
            "Connecting to DB with connection string "
            "postgresql+psycopg2://"
            f"{connection_details['POSTGRES_USER']}:"
            "<password obfuscated>@"
            f"{connection_details['POSTGRES_HOST']}:"
            f"{connection_details['POSTGRES_PORT']}/"
            f"{connection_details['POSTGRES_DB']}"
        )
        try:
            self._sqlalchemy_base = automap_base()
            sqlalchemy_engine = create_engine(
                f"postgresql+psycopg2://{connection_details['POSTGRES_USER']}:"
                f"{connection_details['POSTGRES_PASSWORD']}@"
                f"{connection_details['POSTGRES_HOST']}:"
                f"{connection_details['POSTGRES_PORT']}/"
                f"{connection_details['POSTGRES_DB']}"
            )
            logger.debug("Preparing SQLALchemy base")
            self._sqlalchemy_base.prepare(autoload_with=sqlalchemy_engine)
            logger.debug("Initiating DB session")
            self._session = Session(sqlalchemy_engine)
            logger.debug("Connected to DB")
            self._classes = self._sqlalchemy_base.classes
            logger.debug("Set DB classes")
        except Exception as e:
            logger.error("Failed to connect to DB")
            raise e

    def _get_connection_details(self):
        connection_details = {}
        logger.debug("Getting DB password from secrets manager")
        try:
            secrets_manager = client("secretsmanager")
            password_response = secrets_manager.get_secret_value(
                SecretId=environ.get("POSTGRES_PASSWORD"),
            )
            connection_details["POSTGRES_PASSWORD"] = password_response["SecretString"]
            logger.debug("Got DB password")

            connection_details["POSTGRES_HOST"] = environ.get("POSTGRES_HOST")
            connection_details["POSTGRES_DB"] = environ.get("POSTGRES_DB")
            connection_details["POSTGRES_USER"] = environ.get("POSTGRES_USER")
            connection_details["POSTGRES_PORT"] = environ.get("POSTGRES_PORT")
            for key, value in connection_details.items():
                if value is None:
                    logger.error(f"Missing connection details value: {key}")
                    raise ValueError
            return connection_details
        except Exception as e:
            logger.error("Failed to get connection details for database")
            raise e
