from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from os import environ
from boto3 import client
from json import loads
from pydantic import BaseModel
from dqs_logger import logger


class EventPayload(BaseModel):
    """
    Pydantic model for the payload of the SQS event that triggers the Lambda function

    Attributes:
    file_id: int
    check_id: int
    result_id: int
    """

    file_id: int
    check_id: int
    result_id: int


class Check:
    """
    Class to handle the processing of a data quality check. This class is intended to be used in a Lambda function. The class is initialised with the event payload from the SQS event that triggers the Lambda function. The class provides methods to set the status of the check, and validate the check. The class also provides properties to access the file_id, check_id, and result_id from the event payload. The class also provides properties to access the database session and the data quality task results table.

    Properties:
    result: dqs_taskresults record for the check
    db: Database connection object
    file_id: int
    check_id: int
    result_id: int
    task_results: dqs_taskresults table

    Methods:
    set_status: Set the status of the check
    validate_requested_check: Validate the check
    """

    def __init__(self, lambda_event):
        self._lambda_event = lambda_event
        self._file_id = None
        self._check_id = None
        self._db = None
        self._result_id = None
        self._result = None

    def __str__(self) -> str:
        return f"CheckId: {self._check_id}, FileId: {self._file_id}, ResultId: {self._result_id}"

    @property
    def result(self):
        """
        Property to access the data quality task result record for the check
        """
        try:
            if self._result is None:
                result = self.db.session.scalar(
                    select(self.db.classes.dqs_taskresults).where(
                        self.db.classes.dqs_taskresults.id == self.result_id
                    )
                )
                self._result = result
            return self._result
        except Exception as e:
            logger.error(f"No result record found for result_id {str(self.result_id)}")
            raise e

    @property
    def db(self):
        """
        Property to access the database connection object
        """
        if self._db is None:
            self._db = BodsDB()
        return self._db

    @property
    def file_id(self):
        """
        Property to access the file_id from the event payload
        """
        if self._file_id is None:
            self._extract_test_details_from_event()
        return self._file_id

    @property
    def check_id(self):
        """
        Property to access the check_id from the event payload
        """
        if self._check_id is None:
            self._extract_test_details_from_event()
        return self._check_id

    @property
    def result_id(self):
        """
        Property to access the result_id from the event payload
        """
        if self._result_id is None:
            self._extract_test_details_from_event()
        return self._result_id

    @property
    def task_results(self):
        """
        Property to access the data quality task results table
        """
        if self._task_results_table is None:
            self._task_results_table = self.db.classes.dqs_taskresults
        return self._task_results_table

    def set_status(self, status):
        """
        Method to set the status of the check

        Args:
        status: str
        """
        try:
            self.validate_requested_check()
            logger.debug(
                f"Attempting to set status from {self.result.status} to {status}"
            )
            self.result.status = status
            self.db.session.commit()
        except Exception as e:
            logger.error("Failed to set result status")
            raise e

    def validate_requested_check(self):
        """
        Method to validate the check requested in the event payload is in the database
        """
        logger.debug(f"Validating requested check {str(self.check_id)} is in database")
        returned_id = getattr(self.result, "id", None)
        returned_status = getattr(self.result, "status", None)
        if returned_id != self.result_id:
            logger.error(
                f"Unable to validate check {str(self.result_id)}: Record not returned from DB"
            )
            raise ValueError(
                f"Unable to validate check {str(self.result_id)}: Record not returned from DB"
            )
        elif returned_status != "PENDING":
            logger.error(
                f"Unable to validate check {str(self.result_id)}: Status {returned_status} != PENDING"
            )
            raise ValueError(
                f"Unable to validate check {str(self.result_id)}: Status {returned_status} != PENDING"
            )
        else:
            return True

    def _extract_test_details_from_event(self):
        """
        Method to extract the file_id, check_id, and result_id from the event payload
        """
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
        self._result_id = check_details.result_id


class BodsDB:
    """
    Class to handle the connection to the BODS database. The class provides properties to access the database session and the database classes.

    Properties:
    session: SqlAlchemy session
    classes: List of SqlAlchemy classes autogenerated from the database schema
    """

    def __init__(self):
        self._session = None
        self._classes = None

    @property
    def session(self):
        """
        Property to access the database session
        """
        if self._session is None:
            self._initialise_database()
        return self._session

    @property
    def classes(self):
        """
        Property to access the database classes
        """
        if self._classes is None:
            self._initialise_database()
        return self._classes

    def _initialise_database(self):
        """
        Method to initialise the database connection
        """
        connection_details = self._get_connection_details()
        logger.debug("Connecting to DB with connection string ")
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
        """
        Method to get the connection details for the database from the environment variables
        """
        connection_details = {}
        logger.debug("Getting DB password from secrets manager")
        try:
            secrets_manager = client("secretsmanager")
            if environ.get("POSTGRES_PASSWORD_ARN", None):
                password_response = secrets_manager.get_secret_value(
                    SecretId=environ.get("POSTGRES_PASSWORD_ARN"),
                )
                connection_details["POSTGRES_PASSWORD"] = password_response[
                    "SecretString"
                ]
            else:
                logger.debug(
                    "No password ARN found in environment variables, getting DB password direct"
                )
                connection_details["POSTGRES_PASSWORD"] = environ.get(
                    "POSTGRES_PASSWORD"
                )
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
