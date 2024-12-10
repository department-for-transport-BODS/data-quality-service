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
            queue = multiprocessing.Queue()
            process = multiprocessing.Process(target=target_function, args=(self._event, self._check, queue),)
            # Start the process 
            process.start()
            # Get process output
            process.join(timeout=self._timeout)
            # If the process is still alive after the timeout, terminate it
            if process.is_alive():
                logger.warning("Terminating execution, time exceeded timeout limit.")
                process.terminate()
                raise LambdaTimeOutError("Exiting due to timed out")
            if queue.empty():
                logger.info(f"Returning null from {target_function.__name__}")
                return
            else:
                logger.info(f"Returning value from {target_function.__name__}")
                return queue.get()
        except Exception as e:
            logger.error(f"Error: {e}") 
            raise e