from common import Check
from enums import DQSTaskResultStatus
from dqs_logger import logger
from time_out_handler import TimeOutHandler, get_timeout
from dqs_exception import LambdaTimeOutError


def lambda_worker(event, check) -> None:

    status = DQSTaskResultStatus.DUMMY_SUCCESS.value
    try:
        logger.info("Vanilla lambda for updating the status")

    except Exception as e:
        status = DQSTaskResultStatus.FAILED.value
        logger.error(f"Check status failed due to {e}")
    finally:
        check.set_status(status)

    return


def lambda_handler(event, context):
    try:
        # Get timeout from context reduced by 15 sec
        timeout = get_timeout(context)
        check = Check(event, __name__.split(".")[-1])
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
