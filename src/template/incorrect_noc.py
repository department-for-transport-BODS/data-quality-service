from multiprocessing import Queue

from common import Check
from enums import DQSTaskResultStatus
from organisation_txcfileattributes import OrganisationTxcFileAttributes
from observation_results import ObservationResult
from dqs_logger import logger
from time_out_handler import TimeOutHandler, get_timeout
from dqs_exception import LambdaTimeOutError 

def lambda_worker(event, check, queue: Queue) -> None:

    status = DQSTaskResultStatus.SUCCESS.value
    try:
        observation = ObservationResult(check)
        org_txc_attributes = OrganisationTxcFileAttributes(check)
        logger.info(f"Checking NOC - {org_txc_attributes.org_noc}")
        if not org_txc_attributes.validate_noc_code():
            details = f"The National Operator Code {org_txc_attributes.org_noc} does not match the NOC(s) registered to your BODS organisation profile."
            observation.add_observation(details=details)
            observation.write_observations()
    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
        logger.exception(e)
    finally:
        check.set_status(status)
        logger.info("Check status updated in DB")
    return


def lambda_handler(event, context):
    try:
        # Get timeout from context reduced by 15 sec
        timeout = get_timeout(context)
        check = Check(event, context)
        check.validate_requested_check()
        timeout_handler = TimeOutHandler(event, check, timeout)
        return timeout_handler.run(lambda_worker)
    except LambdaTimeOutError:
        status = DQSTaskResultStatus.TIMEOUT.value 
        logger.info(f"Set status to {status}")
        check.set_status(status)
    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
        check.set_status(status)