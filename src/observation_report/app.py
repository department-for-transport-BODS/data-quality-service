from datetime import datetime
from os import environ
import uuid
import boto3
from dqs_logger import logger
from common import DQSReport
from enums import DQSReportStatus
from dataframes import get_df_dqs_observation_results
from io import StringIO


today_date = datetime.now().strftime('%Y%m%d')
unique_id = uuid.uuid4()

# Initialize S3 client
s3_client = boto3.client('s3')

# Define S3 bucket name and file name
S3_BUCKET_NAME = environ.get("S3_BUCKET_DQS_CSV_REPORT", "bodds-dev-dqs-reports")
CSV_FILE_NAME = f"{today_date}-dqs_observations-{unique_id}.csv"

def lambda_handler(event, context):
    status = DQSReportStatus.REPORT_GENERATED.value

    try:
        report = DQSReport(event)
        report.validate_requested_report_event()

        df = get_df_dqs_observation_results(report)
        logger.info(f"DataFrame size from get_dqs_observation_results: {df.size}")

        if not df.empty:
            logger.info("Generating CSV file from DataFrame")

            # Convert DataFrame to CSV
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False, columns=[
                "importance",
                "category",
                "data_quality_observation",
                "service_code",
                "details",
                "line_name",
                "vehicle_journey_id"
            ])
            
            # Upload CSV to S3
            s3_client.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=CSV_FILE_NAME,
                Body=csv_buffer.getvalue()
            )
            
            logger.info(f"CSV file successfully uploaded to S3 bucket {S3_BUCKET_NAME}")

        logger.info("Check status updated in DB")

    except Exception as e:
        status = DQSReportStatus.REPORT_GENERATION_FAILED.value
        logger.error(f"Check status failed due to {e}")

    finally:
        report.set_status(status)

    return
