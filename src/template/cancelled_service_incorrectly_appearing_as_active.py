from dqs_logger import logger
from common import Check
from enums import DQSTaskResultStatus
from observation_results import ObservationResult
from organisation_txcfileattributes import OrganisationTxcFileAttributes
from otc_service import OtcService
from otc_inactiveservice import OtcInactiveService


def lambda_handler(event, context):

    status = DQSTaskResultStatus.SUCCESS.value
    try:

        check = Check(event)
        observation = ObservationResult(check)
        check.validate_requested_check()

        org_txc_attributes = OrganisationTxcFileAttributes(check)
        logger.info(f"Checking ServiceCode: {org_txc_attributes.service_code}")
        service_code = org_txc_attributes.service_code

        # If the service code starts with UZ, ignore the check
        if service_code.startswith("UZ"):
            logger.info(f"Ignoring check, ServiceCode: {service_code} starts with UZ")
        else:
            # Check for the service in otc_service table
            otc_service = OtcService(check)
            is_service_exists = otc_service.is_service_exists(service_code)
            logger.info(
                f"ServiceCode: {service_code}, Exists: {is_service_exists}, in otc_service "
            )

            # If the service does not exists in otc_service table, check the
            # otc_inactiveservice tbale with effective date later than current date
            if not is_service_exists:
                otc_inactive_service = OtcInactiveService(check)
                is_service_exists = otc_inactive_service.is_service_exists(service_code)
                logger.info(
                    f"ServiceCode: {service_code}, Exists: {is_service_exists}, in otc_inactiveservice "
                )

            if not is_service_exists:
                details = f"The registration number (i.e. service code) {service_code} is not registered with a local bus registrations authority."
                observation.add_observation(details=details)
                logger.info("Observation added in memory")

            # Write the observations to database
            if len(observation.observations) > 0:
                observation.write_observations()
                logger.info("Observations written in DB")

        logger.info("Check status updated in DB")
    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
    finally:
        check.set_status(status)
    return
