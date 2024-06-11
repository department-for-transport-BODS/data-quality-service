from os import environ
from boto3 import client  # noqa
import logging
from sqlalchemy.orm.exc import NoResultFound
from common import Check
from organisation_txcfileattributes import OrganisationTxcFileAttributes
from observation_results import ObservationResult
from dqs_logger import logger


def lambda_handler(event, context) -> None:

    check = Check(event)
    try:
        check.validate_requested_check()
    except ValueError as e:
        logger.error(e)
        check.set_status(status="FAILED")
        return

    status = "SUCCESS"
    observation = ObservationResult(check)
    try:
        org_txc_attributes = OrganisationTxcFileAttributes(check)
        logger.info(f"Checking NOC - {org_txc_attributes.org_noc}")
        if not org_txc_attributes.validate_noc_code():
            details = f"The National Operator Code {org_txc_attributes.org_noc} does not match the NOC(s) registered to your BODS organisation profile."
            observation.add_observation(details=details)
            observation.write_observations()
    except Exception as e:
        logger.error(e)
        status = "FAILED"
    finally:
        check.set_status(status)

    return
