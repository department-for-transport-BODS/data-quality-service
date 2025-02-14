from dqs_report import DQReport
from enums import DQSReportStatus


class TobLevelErrorHandler:
    def __init__(self, revision_id: int):
        if not revision_id:
            raise ValueError("Revision ID is required for TopLevelErrorHandler")
        self.revision_id = revision_id


        

    def get_dq_reports(self):
        dq_report_instance = DQReport()
        dq_reports = dq_report_instance.get_dq_reports_by_revision_id(self.revision_id)
        return dq_reports

    def update_dq_reports(self, dq_reports):
        dq_report_instance = DQReport()
        dq_report_instance.update_dq_reports_status_using_ids(
            dq_reports, DQSReportStatus.PIPELINE_FAILED.value
        )
