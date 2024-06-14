from common import Check
from enums import DQSTaskResultStatus
from dqs_logger import logger

def lambda_handler(event, context):

    status = DQSTaskResultStatus.DUMMY_SUCCESS
    try:
        check = Check(event)
        check.validate_requested_check()
        logger.info("Vanilla lambda for updating the status")

    except Exception as e:
        status = DQSTaskResultStatus.FAILED
        logger.error(f"Check status failed due to {e}")
    finally:
        check.set_status(status)

    return
