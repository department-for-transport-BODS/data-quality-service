import itertools
from dqs_checks import DQChecks
from dqs_report import DQReport
from dqs_logger import logger
from org_txcfileattributes import TXCFileAttributes
from dqs_task_results import DQTaskResults


def get_report_id(revision_id: int) -> int:
    """
    Get DQS Report Id
    """
    report_id = DQReport().initialise_dqs_report(revision_id)
    return report_id


def get_check_ids_list() -> list:
    """
    Get a list of DQS Check Ids
    """
    check_ids = DQChecks().get_all_check_ids()
    return check_ids


def get_txc_files(revision_id: int) -> list:
    """
    Get a list of Organisation TxcFileattributes
    """
    txc_files = TXCFileAttributes().get_all_txc_file_attributes(revision_id=revision_id)
    return txc_files


def lambda_handler(event, context):
    revision_id = event.get("DatasetRevisionId", "")
    try:
        if revision_id:
            report_id = get_report_id(revision_id)
            check_ids = get_check_ids_list()
            txc_files = get_txc_files(revision_id)
            combinations = itertools.product(txc_files, check_ids)
            DQTaskResults().initialize_task_results(report_id, combinations)
            dict_txc_files = list(map(lambda x: {"file_id": x}, txc_files))
            return dict_txc_files
        else:
            logger.error(f"No revision id in event: {event}")

    except Exception as e:
        logger.error(f"Initiate DQS Lambda failed with: {e}")
        logger.exception(e)
