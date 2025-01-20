from common import Check
from enums import DQSTaskResultStatus
from organisation_txcfileattributes import OrganisationTxcFileAttributes
from observation_results import ObservationResult
from dqs_logger import logger
from enums import IgnoredLicenceFormat
from dqs_exception import LambdaTimeOutError 
from time_out_handler import TimeOutHandler, get_timeout

def lambda_worker(event, check) -> None:

    status = DQSTaskResultStatus.SUCCESS.value
    try:
        org_txc_attributes = OrganisationTxcFileAttributes(check)
        licence_number = org_txc_attributes.licence_number
        mode = (
            org_txc_attributes.service_mode.lower()
            if org_txc_attributes.service_mode
            and org_txc_attributes.service_mode.strip() != ""
            else "bus"
        )
        if mode == "coach":
            logger.info(f"Ignoring check, ServiceMode: {mode}")
        elif licence_number.startswith(IgnoredLicenceFormat.UNREGISTERED.value):
            logger.info(f"Ignoring check, LicenseNumber: {licence_number}")
        else:
            observation = ObservationResult(check)
            if not org_txc_attributes.validate_licence_number():
                details = f"The Licence Number {licence_number} does not match the Licence Number(s) registered to your BODS organisation profile."
                observation.add_observation(details=details)
                observation.write_observations()
    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
    finally:
        check.set_status(status)
        logger.info("Check status updated in DB")

    return


def lambda_handler(event, context):
    try:
        # Get timeout from context reduced by 15 sec
        timeout = get_timeout(context)
        check = Check(event)
        check.validate_requested_check()
        timeout_handler = TimeOutHandler(event, check, timeout)
        timeout_handler.run(lambda_worker)
    except LambdaTimeOutError:
        status = DQSTaskResultStatus.TIMEOUT.value 
        logger.info(f"Set status to {status}")
        check.set_status(status)
    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
        check.set_status(status)
