from dqs_logger import logger

def lambda_handler(event, context):
    logger.info(f"Error occurred in lambda_handler with event: {event}")
