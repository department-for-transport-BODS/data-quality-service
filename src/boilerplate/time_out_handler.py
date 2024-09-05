from dqs_logger import logger
from dqs_exception import LambdaTimeOutError
import signal


class TimeOutHandler:
    def __init__(self, context):
        self.context = context
        self.set_time_out()

    def handle_lambda_timeout(self, _signal, _frame):
        raise LambdaTimeOutError("Exiting due to timed out")

    def set_time_out(self):
        signal.signal(signal.SIGALRM, self.handle_lambda_timeout)
        time_limit = int(self.context.get_remaining_time_in_millis() / 1000) - 15
        signal.alarm(time_limit)
        if time_limit < 0:
            logger.warning(f"Time limit is {time_limit}, which is less than 0, alarm can not be set")
