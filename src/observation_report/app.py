from datetime import datetime
from os import environ
import uuid
import boto3
from dqs_logger import logger
from common import DQSReport
from enums import DQSReportStatus
from dataframes import get_df_dqs_observation_results
from io import StringIO

# Initialize S3 client
s3_client = boto3.client('s3')

# Define S3 bucket name and file name
S3_BUCKET_NAME = environ.get("S3_BUCKET_DQS_CSV_REPORT", "bodds-dev-dqs-reports")

def lambda_handler(event, context):
    today_date = datetime.now().strftime('%Y%m%d')
    unique_id = uuid.uuid4()
    status = DQSReportStatus.REPORT_GENERATED.value

    try:
        report = DQSReport(event)
        report.validate_requested_report_event()
        logger.info(f"Report validated successfully")

        df = get_df_dqs_observation_results(report)
        df.drop_duplicates(inplace=True)
        logger.info(f"DataFrame size from observation_results: {df.size}")

        # Convert DataFrame to CSV
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        logger.info(f"CSV Generated: {df.size}")
        csv_content = csv_buffer.getvalue()

        # Upload CSV to S3
        s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=CSV_FILE_NAME, Body=csv_content)
        logger.info(f"CSV file successfully uploaded to S3 bucket {S3_BUCKET_NAME}")

    except Exception as e:
        status = DQSReportStatus.REPORT_GENERATION_FAILED.value
        logger.error(f"Report generation failed due to {e}")

    finally:
        CSV_FILE_NAME = f"BODS_DataQualityReport_{today_date}_{unique_id}_{report._revision_id}.csv"
        report.set_status(status, CSV_FILE_NAME)
        logger.info("Check status updated in DB")

    return
