import json
import os

from dqs_logger import logger
from common import Check
from enums import DQSTaskResultStatus
from ses_helper import SESHelper

status = DQSTaskResultStatus.SENT_TO_DLQ.value

source_email = os.environ.get("SOURCE_EMAIL")
recipient_email = os.environ.get("RECIPIENT_EMAIL")

def lambda_handler(event, context):

    try:
        check = Check(event, context)
        check.validate_requested_check()

        file_id = check.file_id
        check_id = check.check_id
        result_id = check.result_id

        email_body = (
            f"Data Quality Check Notification\n\n"
            f"File ID: {file_id}\n"
            f"Check ID: {check_id}\n"
            f"Result ID: {result_id}\n\n"
            "LAMBDA FAILED TO EXECUTE THIS EVENT - This is an automated message notifying you of the status of the data quality check."
        )
        
        ses_helper = SESHelper(
            source_email=source_email,
            recipient_email=recipient_email
        )

        response = ses_helper.send_email(
            subject='FAILURE-Data Quality Check',
            body=email_body
        )

        logger.info(f"Response from SES {response}")
        
        return {
            'statusCode': 200,
            'body': json.dumps("Email Sent Successfully. MessageId is: " + response['MessageId'])
        }

    except Exception as e:
        logger.error(f"Dead letter queue lambda failed {e}")

    finally:
        check.set_status(status)

    return
