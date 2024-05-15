from os import environ
from boto3 import client  # noqa
import logging
from common import Check

logger = logging.getLogger(__name__)
logger.setLevel(environ.get("LOG_LEVEL", "DEBUG"))
_ANCHOR = '<a class="govuk-link" target="_blank" href="{0}">{0}</a>'
_TRAVEL_LINE_ANCHOR = _ANCHOR.format(
    "https://www.travelinedata.org.uk/traveline-open-data/"
    "transport-operations/browse/"
)


def lambda_handler(event, context):
    ### INITIATE A CHECK BASED ON INCOMING CHECK EVENT

    Check(event)

    print("data")
    ### VALIDATE THAT CHECK ID SENT TO LAMBDA EXISTS AND HAS A STATUS OF PENDING

    # check.validate_requested_check()

    ### ADD AN OBSERVATION FOR YOUR CHECK

    # check.add_observation(
    #     title="Incorrect NOC code",
    #     text=(
    #         "Operators can find their organisation’s NOC by browsing the Traveline NOC "
    #         "database here:"
    #         "</br></br>" + _TRAVEL_LINE_ANCHOR + "</br></br>"
    #         "Operators can assign a NOC to their account on this service by going to My "
    #         "account (in the top right-hand side of the dashboard) and choosing "
    #         "Organisation profile. "
    #     ),
    #     impacts=(
    #         "The NOC is used by consumers to know which operator is running the service, "
    #         "and to match their data across data types. This ability improves "
    #         "the quality of information available to passengers."
    #     ),
    #     model=check.db.classes.data_quality_incorrectnocwarning,
    #     list_url_name="dq:incorrect-noc-list",
    #     level=Level.critical,
    #     category=Category.data_set,
    #     weighting=0.12,
    #     check_basis=CheckBasis.data_set,
    # )
    # check.add_observation(
    #     service_pattern_stop_id= 1,
    #     details = "Added Service Pattern Stop ID"
    # )

    ### WRITE ALL OBSERVATIONS TO DATABASE

    # check.write_observations()

    ### UPDATE CHECK STATUS FOLLOWING COMPLETION OF CHECKS

    # check.set_status("SUCCESS")
    return
