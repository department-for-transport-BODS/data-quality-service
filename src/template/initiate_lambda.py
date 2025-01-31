import itertools
from regex import D
from boilerplate.common import Check
from boilerplate.dqs_checks import DQChecks, DQ
from boilerplate.dqs_report import DQReport
from boilerplate.dqs_logger import logger
from boilerplate.org_txcfileattributes import TXCFileAttributes
from boilerplate.organisation_datasetrevision import Revision
from boilerplate.dqs_task_results import DQTaskResults
def lambda_handler(event, context):
        
    revision_id = event.get('revision_id','')
    if revision_id:
        revision = Revision.get_revision(revision_id)
        report = DQReport.initialise_dqs_task(revision)
        logger.info(f"report ${report}")
        checks = DQChecks.get_all_checks()
        txc_files = TXCFileAttributes.get_all_txc_file_attributes(revision_id=revision_id)
        combinations = itertools.product(txc_files, checks)
        DQTaskResults.initialize_task_results(report, combinations)
    else:
        logger.error(f"No revision id in even: {event}")

    logger.info(f"txc_files are: {txc_files}")
    return txc_files

