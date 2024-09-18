from common import Check
from enums import DQSTaskResultStatus
from organisation_txcfileattributes import OrganisationTxcFileAttributes
from observation_results import ObservationResult
from dqs_logger import logger
from time_out_handler import TimeOutHandler
from dqs_exception import LambdaTimeOutError 

def lambda_handler(event, context) -> None:

    status = DQSTaskResultStatus.SUCCESS.value
    try:
        check = Check(event)
        observation = ObservationResult(check)
        check.validate_requested_check()

        org_txc_attributes = OrganisationTxcFileAttributes(check)
        logger.info(f"Checking NOC - {org_txc_attributes.org_noc}")
        if not org_txc_attributes.validate_noc_code():
            details = f"The National Operator Code {org_txc_attributes.org_noc} does not match the NOC(s) registered to your BODS organisation profile."
            observation.add_observation(details=details)
            observation.write_observations()
    except LambdaTimeOutError as e:
        status = DQSTaskResultStatus.TIMEOUT.value
        logger.error(f"Check status timed out due to {e}")
    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
    finally:
        check.set_status(status)
        logger.info("Check status updated in DB")
    return
