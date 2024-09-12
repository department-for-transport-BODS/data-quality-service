import boto3
import pandas as pd
import urllib.parse
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from os import environ
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

class ReportEventPayload(BaseModel):
    """
    Pydantic model for the payload of the SQS event that triggers the Lambda function for DQS report generation

    Attributes:
    report_id: int
    """

    report_id: int


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
        logger.debug("Connecting to DB with connection string")
        try:
            self._sqlalchemy_base = automap_base()
            sqlalchemy_engine = create_engine(
                self._generate_connection_string(**connection_details)
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
        connection_details["host"] = environ.get("POSTGRES_HOST")
        connection_details["dbname"] = environ.get("POSTGRES_DB")
        connection_details["user"] = environ.get("POSTGRES_USER")
        connection_details["port"] = environ.get("POSTGRES_PORT")
        try:
            if environ.get("PROJECT_ENV") != 'local':
                logger.debug("Getting DB token")
                connection_details["password"] = self._generate_rds_iam_auth_token(
                    connection_details["host"],
                    connection_details["port"],
                    connection_details["user"]
                )
                logger.debug("Got DB token")
                connection_details["sslmode"] = "require"
            else:
                logger.debug("No password ARN found in environment variables, getting DB password direct")
                connection_details["password"] = environ.get("POSTGRES_PASSWORD")
                logger.debug("Got DB password")
                connection_details["sslmode"] = "disable"

            for key, value in connection_details.items():
                if value is None:
                    logger.error(f"Missing connection details value: {key}")
                    raise ValueError
            return connection_details
        except Exception as e:
            logger.error("Failed to get connection details for database")
            raise e

    def _generate_connection_string(self, **kwargs) -> str:
        """
        Generates an AWS RDS IAM authentication token for a given RDS instance.

        Parameters:
        - **kwargs (any): A dictionary of key/value pairs that correspond to the expected values below

        Returns:
        - str: The generated connection string from parsed key/value pairs
        """
        user_password = ""
        if kwargs.get("user"):
            user_password += kwargs.get("user")
            if kwargs.get("password"):
                user_password += ":" + kwargs.get("password")
            user_password += "@"

        # Construct other parts
        other_parts = ""
        for key, value in kwargs.items():
            if key not in ["host", "port", "user", "password", "dbname"] and value:
                other_parts += f"{key}={value}&"

        # Construct the final connection string
        connection_string = f"postgresql+psycopg2://{user_password}{kwargs.get('host', '')}"
        if kwargs.get("port"):
            connection_string += f":{kwargs.get('port')}"
        connection_string += f"/{kwargs.get('dbname', '')}"
        if other_parts:
            connection_string += f"?{other_parts[:-1]}"

        return connection_string

    def _generate_rds_iam_auth_token(self, host, port, username) -> str:
        """
        Generates an AWS RDS IAM authentication token for a given RDS instance.

        Parameters:
        - hostname (str): The endpoint of the RDS instance.
        - port (int): The port number for the RDS instance.
        - username (str): The database username.

        Returns:
        - str: The generated IAM authentication token if successful.
        - None: If an error occurs during token generation.
        """
        try:
            session = boto3.session.Session()
            client = session.client(
                service_name="rds",
                region_name=environ.get("AWS_REGION")
            )
            token = client.generate_db_auth_token(
                DBHostname=host,
                DBUsername=username,
                Port=port
            )
            return urllib.parse.quote_plus(token)
        except Exception as e:
            logger.error(f"An error occurred while generating the IAM auth token: {e}")
            return None


class DQSReport:
    """
    Class to handle the processing of a data quality report generation. This class is intended to be used in a Lambda function. The class is initialised with the event payload from the SQS event that triggers the Lambda function. The class provides methods to set the status of the event, and validate the event.
    """

    def __init__(self, lambda_event):
        self._lambda_event = lambda_event
        self._report_id = None
        self._db = None
        self._report = None
        self._revision_id = None
        self._dataset_id = None

    def __str__(self) -> str:
        return f"ReportId: {self._report_id}"

    @property
    def db(self):
        """
        Property to access the database connection object
        """
        if self._db is None:
            self._db = BodsDB()
        return self._db

    @property
    def report_id(self):
        """
        Property to access the report_id from the event payload
        """
        if self._report_id is None:
            self._extract_report_details_from_event()
        return self._report_id

    @property
    def report(self):
        """
        Property to access the data quality report record for the validation
        """
        if self._report is None:
            try:
                report = self.db.session.scalar(
                    select(self.db.classes.dqs_report).where(
                        self.db.classes.dqs_report.id == self.report_id
                    )
                )
                self._report = report
            except Exception as e:
                logger.error(f"No report record found for report_id {str(self.report_id)}")
                raise e
        return self._report
    
    @property
    def revision_id(self):
        """
        Property to access the revision_id of the report
        """

        if self._revision_id is None:
            self._get_revision()
        return self._revision_id
    
    @property
    def dataset_id(self):
        """
        Property to acess the dataset_id of the report revision_id
        """

        if self._dataset_id is None:
            self._get_organisation_dataset()
        return self._dataset_id
    
    
    def _get_revision(self):
        """
        Property to access the revision_id from the report.
        If report is not available, it fetches the report first.
        """
        try:
            if self.report is not None:
                self._revision_id = self.report.revision_id
            else:
                raise ValueError("Report is not available to fetch the revision_id.")
        except Exception as e:
            logger.error(f"Failed to retrieve revision_id: {e}")
            raise e
    

    def _get_organisation_dataset(self):
        """
        Method to get the organisation dataset
        """
        OrganisationDatasetRevision = self.db.classes.organisation_datasetrevision
        try:
            result = (
                self.db.session.query(OrganisationDatasetRevision)
                .where(OrganisationDatasetRevision.id == self.revision_id)
                .first()
            )
            self._dataset_id = result.dataset_id
        except Exception as e:
            logger.error(
                f"Attempting to fetch details of organisation_dataset for id = {str(self._report_id)}",
                e,
            )
            raise e

    def set_status(self, status, file_name):
        """
        Method to set the status of the check

        Args:
        status: str
        """
        try:
            self.validate_requested_report_event()
            logger.debug(f"Attempting to set status from {self.report.status} to {status}")
            self.report.status = status
            self.report.file_name = file_name
            self.db.session.commit()
        except Exception as e:
            logger.error("Failed to set report status")
            raise e

    def validate_requested_report_event(self):
        """
        Method to validate the report_id requested in the event payload is in the database
        """
        logger.debug(f"Validating requested report {str(self.report_id)} is in database")
        if self.report is None:
            logger.error(f"Unable to validate report {str(self.report_id)}: No report found")
            raise ValueError(f"Unable to validate report {str(self.report_id)}: No report found")
        
        returned_id = getattr(self.report, "id", None)
        returned_status = getattr(self.report, "status", None)

        logger.info(f"The returned id is {returned_id} and returned status is {returned_status}")
        
        if returned_id != self.report_id:
            logger.error(f"Unable to validate report {str(self.report_id)}: Record not returned from DB")
            raise ValueError(f"Unable to validate report {str(self.report_id)}: Record not returned from DB")
        elif returned_status not in ["PIPELINE_SUCCEEDED", "PIPELINE_SUCCEEDED_WITH_ERRORS"]:
            logger.error(f"Unable to validate report {str(self.report_id)}: Status {returned_status}")
            raise ValueError(f"Unable to validate report {str(self.report_id)}: Status {returned_status}")
        else:
            return True

    def _extract_report_details_from_event(self):
        """
        Method to extract the report_id from the event payload
        """
        logger.debug("Event received:")
        logger.debug(self._lambda_event)
        try:
            event_payload = loads(self._lambda_event["Records"][0]["body"])
            logger.debug("Extracted report payload from event:")
            logger.debug(event_payload)
            report_payload_details = ReportEventPayload(**event_payload)
        except Exception as e:
            logger.error("Failed to extract a valid payload from the event")
            raise e
        logger.debug(f"Report details found for report_id={str(report_payload_details.report_id)}")
        self._report_id = report_payload_details.report_id
