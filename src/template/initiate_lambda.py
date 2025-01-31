import itertools
from dqs_checks import DQChecks
from dqs_report import DQReport
from dqs_logger import logger
from org_txcfileattributes import TXCFileAttributes
from organisation_datasetrevision import Revision
from dqs_task_results import DQTaskResults

def lambda_handler(event, context):
    revision_id = event.get('revision_id','')
    if revision_id:
        revision = Revision().get_revision(revision_id)
        report_id = DQReport().initialise_dqs_task(revision)
        logger.info(f"report ${report_id}")
        checks = DQChecks().get_all_checks()
        txc_files = TXCFileAttributes().get_all_txc_file_attributes(revision_id=revision_id)
        combinations = itertools.product(txc_files, checks)
        DQTaskResults().initialize_task_results(report_id, combinations)
    else:
        logger.error(f"No revision id in even: {event}")

    logger.info(f"txc_files are: {txc_files}")
    return txc_files

