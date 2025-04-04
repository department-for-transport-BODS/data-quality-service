from sqlalchemy import select, func
from json import loads
from pydantic import BaseModel
from bods_db import BodsDB
from dqs_logger import logger
from models import DqsTaskresults, DqsChecks, DqsReport, OrganisationDatasetrevision


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

    def __init__(self, lambda_event, function_name):
        self._lambda_function = function_name
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
                    select(DqsTaskresults).where(DqsTaskresults.id == self.result_id)
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
            self._task_results_table = DqsTaskresults
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
                f"Attempting to set {self.result.id} status from {self.result.status} to {status}"
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

    def get_check_id(self):
        logger.debug(f"Retrieving check ID for {self._lambda_function}")
        check = self.db.session.scalar(
            select(DqsChecks).where(
                func.replace(func.lower(DqsChecks.observation), " ", "_")
                == self._lambda_function
            )
        )
        return check.id if check else 0

    def get_result_id(self, file_id, check_id):
        result = self.db.session.scalar(
            select(DqsTaskresults).where(
                (DqsTaskresults.transmodel_txcfileattributes_id == file_id)
                & (DqsTaskresults.checks_id == check_id)
            )
        )
        return result.id if result else 0

    def _extract_test_details_from_event(self):
        """
        Method to extract the file_id, check_id, and result_id from the event payload
        """
        logger.debug("Event received:")
        logger.debug(self._lambda_event)
        if "Records" not in self._lambda_event.keys():
            logger.debug("Processing Non-Record Event, assuming from state machine")
            try:
                check_id = self.get_check_id()
                result_id = self.get_result_id(
                    self._lambda_event.get("file_id"), check_id
                )
                check_details = EventPayload(
                    check_id=check_id,
                    result_id=result_id,
                    file_id=self._lambda_event.get("file_id"),
                    previous_result=self._lambda_event.get("previous_result", None),
                )
            except Exception as e:
                logger.error("Failed to create EventPayload from event")
                logger.exception(e)
                raise e
        else:
            logger.debug("Processing Event with Records, assuming from SQS")
            try:
                event_payload = loads(self._lambda_event["Records"][0]["body"])
                logger.debug("Extracted Payload from event:")
                logger.debug(event_payload)
                logger.debug("Checking payload has required fields")
                check_details = EventPayload(**event_payload)
            except Exception as e:
                logger.error("Failed to extract a valid payload from the event")
                logger.exception(e)
                raise e
        logger.debug(
            f"Check_details found. TXC file ID={str(check_details.file_id)}, check ID={str(check_details.check_id)}"
        )
        self._file_id = check_details.file_id
        self._check_id = check_details.check_id
        self._result_id = check_details.result_id


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
                    select(DqsReport).where(DqsReport.id == self.report_id)
                )
                self._report = report
            except Exception as e:
                logger.error(
                    f"No report record found for report_id {str(self.report_id)}"
                )
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
        try:
            result = (
                self.db.session.query(OrganisationDatasetrevision)
                .where(OrganisationDatasetrevision.id == self.revision_id)
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
            logger.debug(
                f"Attempting to set status from {self.report.status} to {status}"
            )
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
        logger.debug(
            f"Validating requested report {str(self.report_id)} is in database"
        )
        if self.report is None:
            logger.error(
                f"Unable to validate report {str(self.report_id)}: No report found"
            )
            raise ValueError(
                f"Unable to validate report {str(self.report_id)}: No report found"
            )

        returned_id = getattr(self.report, "id", None)
        returned_status = getattr(self.report, "status", None)

        logger.info(
            f"The returned id is {returned_id} and returned status is {returned_status}"
        )

        if returned_id != self.report_id:
            logger.error(
                f"Unable to validate report {str(self.report_id)}: Record not returned from DB"
            )
            raise ValueError(
                f"Unable to validate report {str(self.report_id)}: Record not returned from DB"
            )
        elif returned_status not in [
            "PIPELINE_SUCCEEDED",
            "PIPELINE_SUCCEEDED_WITH_ERRORS",
        ]:
            logger.error(
                f"Unable to validate report {str(self.report_id)}: Status {returned_status}"
            )
            raise ValueError(
                f"Unable to validate report {str(self.report_id)}: Status {returned_status}"
            )
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
        logger.debug(
            f"Report details found for report_id={str(report_payload_details.report_id)}"
        )
        self._report_id = report_payload_details.report_id
