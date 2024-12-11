from json import load
from os.path import exists

from dqs_logger import logger
from dqs_exception import LambdaTimeOutError
import multiprocessing

def get_timeout(context):
    """Return timeout reduced 15 sec."""
    return int(context.get_remaining_time_in_millis() / 1000) - 15

class TimeOutHandler:
    def __init__(self,event,check,timeout):
        self._event = event
        self._check = check
        self._timeout = timeout

    def run(self,target_function,*args):
        """
        Take function as argument and running in separated process
        """
        try:
            # Set start method if is already set then silent the error.
            try:
                multiprocessing.set_start_method('fork')
            except Exception:
                pass
            parent_conn, child_conn = multiprocessing.Pipe()
            process = multiprocessing.Process(target=target_function, args=(self._event, self._check, child_conn),)
            # Start the process 
            process.start()
            # Get process output
            process.join(timeout=self._timeout - 30)
            # If the process is still alive after the timeout, terminate it
            if process.is_alive():
                logger.warning("Terminating execution, time exceeded timeout limit.")
                process.terminate()
                raise LambdaTimeOutError("Exiting due to timed out")

            out_file = f"/tmp/df-output-{self._check.file_id}"
            if exists(out_file):
                with open(out_file, "r") as f:
                    result = load(f)
                logger.info(f"Returning value from {target_function.__name__}")
                return result
            else:
                logger.info(f"Returning null from {target_function.__name__}")
        except Exception as e:
            logger.error(f"Error: {e}") 
            raise e