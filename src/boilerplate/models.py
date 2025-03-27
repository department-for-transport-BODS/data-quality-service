from typing import Any, List, Optional

from geoalchemy2.types import Geometry
from sqlalchemy import ARRAY, BigInteger, Boolean, Date, DateTime, Double, Identity, Integer, Numeric, Sequence, SmallInteger, String, Text, Time, Uuid
from sqlalchemy.dialects.postgresql import INTERVAL, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal
import uuid

class Base(DeclarativeBase):
    pass


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150))

    users_user_groups: Mapped[List['UsersUserGroups']] = relationship('UsersUserGroups', back_populates='group')
    waffle_flag_groups: Mapped[List['WaffleFlagGroups']] = relationship('WaffleFlagGroups', back_populates='group')
    auth_group_permissions: Mapped[List['AuthGroupPermissions']] = relationship('AuthGroupPermissions', back_populates='group')


class AvlCavldataarchive(Base):
    __tablename__ = 'avl_cavldataarchive'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    data: Mapped[str] = mapped_column(String(100))
    data_format: Mapped[str] = mapped_column(String(2))


class ChangelogHighlevelroadmap(Base):
    __tablename__ = 'changelog_highlevelroadmap'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    description: Mapped[str] = mapped_column(Text)


class ChangelogKnownissues(Base):
    __tablename__ = 'changelog_knownissues'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20))
    deleted: Mapped[bool] = mapped_column(Boolean)


class DataQualityChecks(Base):
    __tablename__ = 'data_quality_checks'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    observation: Mapped[str] = mapped_column(String(1024))
    importance: Mapped[str] = mapped_column(String(64))
    category: Mapped[str] = mapped_column(String(64))

    data_quality_taskresults: Mapped[List['DataQualityTaskresults']] = relationship('DataQualityTaskresults', back_populates='checks')


class DataQualityService(Base):
    __tablename__ = 'data_quality_service'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    ito_id: Mapped[str] = mapped_column(Text)

    data_quality_lineexpiredwarning: Mapped[List['DataQualityLineexpiredwarning']] = relationship('DataQualityLineexpiredwarning', back_populates='service')
    data_quality_linemissingblockidwarning: Mapped[List['DataQualityLinemissingblockidwarning']] = relationship('DataQualityLinemissingblockidwarning', back_populates='service')
    data_quality_service_reports: Mapped[List['DataQualityServiceReports']] = relationship('DataQualityServiceReports', back_populates='service')


class DataQualityServicepatternservicelink(Base):
    __tablename__ = 'data_quality_servicepatternservicelink'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position: Mapped[int] = mapped_column(Integer)
    service_link_id: Mapped[int] = mapped_column(Integer)
    service_pattern_id: Mapped[int] = mapped_column(Integer)


class DataQualityServicepatternstop(Base):
    __tablename__ = 'data_quality_servicepatternstop'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position: Mapped[int] = mapped_column(Integer)
    service_pattern_id: Mapped[int] = mapped_column(Integer)
    stop_id: Mapped[int] = mapped_column(Integer)

    data_quality_timingpatternstop: Mapped[List['DataQualityTimingpatternstop']] = relationship('DataQualityTimingpatternstop', back_populates='service_pattern_stop')


class DataQualityTimingpattern(Base):
    __tablename__ = 'data_quality_timingpattern'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_pattern_id: Mapped[int] = mapped_column(Integer)
    ito_id: Mapped[str] = mapped_column(Text)

    data_quality_timingpatternstop: Mapped[List['DataQualityTimingpatternstop']] = relationship('DataQualityTimingpatternstop', back_populates='timing_pattern')
    data_quality_vehiclejourney: Mapped[List['DataQualityVehiclejourney']] = relationship('DataQualityVehiclejourney', back_populates='timing_pattern')
    data_quality_fastlinkwarning: Mapped[List['DataQualityFastlinkwarning']] = relationship('DataQualityFastlinkwarning', back_populates='timing_pattern')
    data_quality_fasttimingwarning: Mapped[List['DataQualityFasttimingwarning']] = relationship('DataQualityFasttimingwarning', back_populates='timing_pattern')
    data_quality_slowlinkwarning: Mapped[List['DataQualitySlowlinkwarning']] = relationship('DataQualitySlowlinkwarning', back_populates='timing_pattern')
    data_quality_slowtimingwarning: Mapped[List['DataQualitySlowtimingwarning']] = relationship('DataQualitySlowtimingwarning', back_populates='timing_pattern')
    data_quality_timingbackwardswarning: Mapped[List['DataQualityTimingbackwardswarning']] = relationship('DataQualityTimingbackwardswarning', back_populates='timing_pattern')
    data_quality_timingdropoffwarning: Mapped[List['DataQualityTimingdropoffwarning']] = relationship('DataQualityTimingdropoffwarning', back_populates='timing_pattern')
    data_quality_timingfirstwarning: Mapped[List['DataQualityTimingfirstwarning']] = relationship('DataQualityTimingfirstwarning', back_populates='timing_pattern')
    data_quality_timinglastwarning: Mapped[List['DataQualityTiminglastwarning']] = relationship('DataQualityTiminglastwarning', back_populates='timing_pattern')
    data_quality_timingmissingpointwarning: Mapped[List['DataQualityTimingmissingpointwarning']] = relationship('DataQualityTimingmissingpointwarning', back_populates='timing_pattern')
    data_quality_timingmultiplewarning: Mapped[List['DataQualityTimingmultiplewarning']] = relationship('DataQualityTimingmultiplewarning', back_populates='timing_pattern')
    data_quality_timingpickupwarning: Mapped[List['DataQualityTimingpickupwarning']] = relationship('DataQualityTimingpickupwarning', back_populates='timing_pattern')


class DisruptionsDisruptionsdataarchive(Base):
    __tablename__ = 'disruptions_disruptionsdataarchive'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    data: Mapped[str] = mapped_column(String(100))


class DjangoCeleryBeatClockedschedule(Base):
    __tablename__ = 'django_celery_beat_clockedschedule'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clocked_time: Mapped[datetime.datetime] = mapped_column(DateTime(True))

    django_celery_beat_periodictask: Mapped[List['DjangoCeleryBeatPeriodictask']] = relationship('DjangoCeleryBeatPeriodictask', back_populates='clocked')


class DjangoCeleryBeatCrontabschedule(Base):
    __tablename__ = 'django_celery_beat_crontabschedule'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    minute: Mapped[str] = mapped_column(String(240))
    hour: Mapped[str] = mapped_column(String(96))
    day_of_week: Mapped[str] = mapped_column(String(64))
    day_of_month: Mapped[str] = mapped_column(String(124))
    month_of_year: Mapped[str] = mapped_column(String(64))
    timezone: Mapped[str] = mapped_column(String(63))

    django_celery_beat_periodictask: Mapped[List['DjangoCeleryBeatPeriodictask']] = relationship('DjangoCeleryBeatPeriodictask', back_populates='crontab')


class DjangoCeleryBeatIntervalschedule(Base):
    __tablename__ = 'django_celery_beat_intervalschedule'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    every: Mapped[int] = mapped_column(Integer)
    period: Mapped[str] = mapped_column(String(24))

    django_celery_beat_periodictask: Mapped[List['DjangoCeleryBeatPeriodictask']] = relationship('DjangoCeleryBeatPeriodictask', back_populates='interval')


class DjangoCeleryBeatPeriodictasks(Base):
    __tablename__ = 'django_celery_beat_periodictasks'

    ident: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    last_update: Mapped[datetime.datetime] = mapped_column(DateTime(True))


class DjangoCeleryBeatSolarschedule(Base):
    __tablename__ = 'django_celery_beat_solarschedule'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event: Mapped[str] = mapped_column(String(24))
    latitude: Mapped[decimal.Decimal] = mapped_column(Numeric(9, 6))
    longitude: Mapped[decimal.Decimal] = mapped_column(Numeric(9, 6))

    django_celery_beat_periodictask: Mapped[List['DjangoCeleryBeatPeriodictask']] = relationship('DjangoCeleryBeatPeriodictask', back_populates='solar')


class DjangoCeleryResultsChordcounter(Base):
    __tablename__ = 'django_celery_results_chordcounter'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[str] = mapped_column(String(255))
    sub_tasks: Mapped[str] = mapped_column(Text)
    count: Mapped[int] = mapped_column(Integer)


class DjangoCeleryResultsGroupresult(Base):
    __tablename__ = 'django_celery_results_groupresult'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[str] = mapped_column(String(255))
    date_created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    date_done: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    content_type: Mapped[str] = mapped_column(String(128))
    content_encoding: Mapped[str] = mapped_column(String(64))
    result: Mapped[Optional[str]] = mapped_column(Text)


class DjangoCeleryResultsTaskresult(Base):
    __tablename__ = 'django_celery_results_taskresult'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50))
    content_type: Mapped[str] = mapped_column(String(128))
    content_encoding: Mapped[str] = mapped_column(String(64))
    date_done: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    date_created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    result: Mapped[Optional[str]] = mapped_column(Text)
    traceback: Mapped[Optional[str]] = mapped_column(Text)
    meta: Mapped[Optional[str]] = mapped_column(Text)
    task_args: Mapped[Optional[str]] = mapped_column(Text)
    task_kwargs: Mapped[Optional[str]] = mapped_column(Text)
    task_name: Mapped[Optional[str]] = mapped_column(String(255))
    worker: Mapped[Optional[str]] = mapped_column(String(100))
    periodic_task_name: Mapped[Optional[str]] = mapped_column(String(255))


class DjangoContentType(Base):
    __tablename__ = 'django_content_type'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    app_label: Mapped[str] = mapped_column(String(100))
    model: Mapped[str] = mapped_column(String(100))

    auth_permission: Mapped[List['AuthPermission']] = relationship('AuthPermission', back_populates='content_type')
    django_admin_log: Mapped[List['DjangoAdminLog']] = relationship('DjangoAdminLog', back_populates='content_type')


class DjangoMigrations(Base):
    __tablename__ = 'django_migrations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    app: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    applied: Mapped[datetime.datetime] = mapped_column(DateTime(True))


class DjangoSession(Base):
    __tablename__ = 'django_session'

    session_key: Mapped[str] = mapped_column(String(40), primary_key=True)
    session_data: Mapped[str] = mapped_column(Text)
    expire_date: Mapped[datetime.datetime] = mapped_column(DateTime(True))


class DjangoSite(Base):
    __tablename__ = 'django_site'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    domain: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(50))


class DqsChecks(Base):
    __tablename__ = 'dqs_checks'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    observation: Mapped[str] = mapped_column(String(1024))
    importance: Mapped[str] = mapped_column(String(64))
    category: Mapped[str] = mapped_column(String(64))
    queue_name: Mapped[Optional[str]] = mapped_column(String(256))

    dqs_taskresults: Mapped[List['DqsTaskresults']] = relationship('DqsTaskresults', back_populates='checks')


class FeedbackFeedback(Base):
    __tablename__ = 'feedback_feedback'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date)
    page_url: Mapped[str] = mapped_column(String(2048))
    satisfaction_rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(String(1200))


class NaptanDistrict(Base):
    __tablename__ = 'naptan_district'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    naptan_locality: Mapped[List['NaptanLocality']] = relationship('NaptanLocality', back_populates='district')


class OrganisationDataset(Base):
    __tablename__ = 'organisation_dataset'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    organisation_id: Mapped[int] = mapped_column(Integer)
    contact_id: Mapped[int] = mapped_column(Integer)
    dataset_type: Mapped[int] = mapped_column(Integer)
    avl_feed_status: Mapped[str] = mapped_column(String(20))
    is_dummy: Mapped[bool] = mapped_column(Boolean)
    live_revision_id: Mapped[Optional[int]] = mapped_column(Integer)
    avl_feed_last_checked: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    contact: Mapped['UsersUser'] = relationship('UsersUser', back_populates='organisation_dataset')
    live_revision: Mapped[Optional['OrganisationDatasetrevision']] = relationship('OrganisationDatasetrevision', back_populates='organisation_dataset')
    organisation: Mapped['OrganisationOrganisation'] = relationship('OrganisationOrganisation', back_populates='organisation_dataset')
    organisation_datasetrevision: Mapped[List['OrganisationDatasetrevision']] = relationship('OrganisationDatasetrevision', back_populates='dataset')
    avl_postpublishingcheckreport: Mapped[List['AvlPostpublishingcheckreport']] = relationship('AvlPostpublishingcheckreport', back_populates='dataset')
    organisation_avlcompliancecache: Mapped[List['OrganisationAvlcompliancecache']] = relationship('OrganisationAvlcompliancecache', back_populates='dataset')
    organisation_datasetsubscription: Mapped[List['OrganisationDatasetsubscription']] = relationship('OrganisationDatasetsubscription', back_populates='dataset')
    organisation_consumerfeedback: Mapped[List['OrganisationConsumerfeedback']] = relationship('OrganisationConsumerfeedback', back_populates='dataset')


class OrganisationDatasetrevision(Base):
    __tablename__ = 'organisation_datasetrevision'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    status: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    comment: Mapped[str] = mapped_column(String(255))
    is_published: Mapped[bool] = mapped_column(Boolean)
    url_link: Mapped[str] = mapped_column(String(500))
    transxchange_version: Mapped[str] = mapped_column(String(8))
    dataset_id: Mapped[int] = mapped_column(Integer)
    password: Mapped[str] = mapped_column(String(255))
    requestor_ref: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(255))
    short_description: Mapped[str] = mapped_column(String(30))
    modified_file_hash: Mapped[str] = mapped_column(String(40))
    original_file_hash: Mapped[str] = mapped_column(String(40))
    upload_file: Mapped[Optional[str]] = mapped_column(String(100))
    num_of_lines: Mapped[Optional[int]] = mapped_column(Integer)
    num_of_operators: Mapped[Optional[int]] = mapped_column(Integer)
    imported: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    bounding_box: Mapped[Optional[str]] = mapped_column(String(8096))
    publisher_creation_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    publisher_modified_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    first_expiring_service: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    last_expiring_service: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    first_service_start: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    num_of_bus_stops: Mapped[Optional[int]] = mapped_column(Integer)
    last_modified_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    published_by_id: Mapped[Optional[int]] = mapped_column(Integer)
    published_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    num_of_timing_points: Mapped[Optional[int]] = mapped_column(Integer)

    organisation_dataset: Mapped[List['OrganisationDataset']] = relationship('OrganisationDataset', back_populates='live_revision')
    dataset: Mapped['OrganisationDataset'] = relationship('OrganisationDataset', back_populates='organisation_datasetrevision')
    last_modified_user: Mapped[Optional['UsersUser']] = relationship('UsersUser', back_populates='organisation_datasetrevision')
    published_by: Mapped[Optional['UsersUser']] = relationship('UsersUser', back_populates='organisation_datasetrevision_')
    avl_avlvalidationreport: Mapped[List['AvlAvlvalidationreport']] = relationship('AvlAvlvalidationreport', back_populates='revision')
    avl_cavlvalidationtaskresult: Mapped[List['AvlCavlvalidationtaskresult']] = relationship('AvlCavlvalidationtaskresult', back_populates='revision')
    data_quality_dataqualityreport: Mapped[List['DataQualityDataqualityreport']] = relationship('DataQualityDataqualityreport', back_populates='revision')
    data_quality_postschemaviolation: Mapped[List['DataQualityPostschemaviolation']] = relationship('DataQualityPostschemaviolation', back_populates='revision')
    data_quality_ptiobservation: Mapped[List['DataQualityPtiobservation']] = relationship('DataQualityPtiobservation', back_populates='revision')
    data_quality_ptivalidationresult: Mapped[List['DataQualityPtivalidationresult']] = relationship('DataQualityPtivalidationresult', back_populates='revision')
    data_quality_report: Mapped[List['DataQualityReport']] = relationship('DataQualityReport', back_populates='revision')
    data_quality_schemaviolation: Mapped[List['DataQualitySchemaviolation']] = relationship('DataQualitySchemaviolation', back_populates='revision')
    dqs_report: Mapped[List['DqsReport']] = relationship('DqsReport', back_populates='revision')
    organisation_datasetmetadata: Mapped[List['OrganisationDatasetmetadata']] = relationship('OrganisationDatasetmetadata', back_populates='revision')
    organisation_txcfileattributes: Mapped[List['OrganisationTxcfileattributes']] = relationship('OrganisationTxcfileattributes', back_populates='revision')
    pipelines_datasetetlerror: Mapped[List['PipelinesDatasetetlerror']] = relationship('PipelinesDatasetetlerror', back_populates='revision')
    pipelines_datasetetltaskresult: Mapped[List['PipelinesDatasetetltaskresult']] = relationship('PipelinesDatasetetltaskresult', back_populates='revision')
    pipelines_fileprocessingresult: Mapped[List['PipelinesFileprocessingresult']] = relationship('PipelinesFileprocessingresult', back_populates='revision')
    pipelines_remotedatasethealthcheckcount: Mapped[List['PipelinesRemotedatasethealthcheckcount']] = relationship('PipelinesRemotedatasethealthcheckcount', back_populates='revision')
    transmodel_servicepattern: Mapped[List['TransmodelServicepattern']] = relationship('TransmodelServicepattern', back_populates='revision')
    fares_validator_faresvalidation: Mapped[List['FaresValidatorFaresvalidation']] = relationship('FaresValidatorFaresvalidation', back_populates='revision')
    fares_validator_faresvalidationresult: Mapped[List['FaresValidatorFaresvalidationresult']] = relationship('FaresValidatorFaresvalidationresult', back_populates='revision')
    organisation_datasetrevision_admin_areas: Mapped[List['OrganisationDatasetrevisionAdminAreas']] = relationship('OrganisationDatasetrevisionAdminAreas', back_populates='datasetrevision')
    pipelines_dataqualitytask: Mapped[List['PipelinesDataqualitytask']] = relationship('PipelinesDataqualitytask', back_populates='revision')
    transmodel_service: Mapped[List['TransmodelService']] = relationship('TransmodelService', back_populates='revision')
    organisation_datasetrevision_localities: Mapped[List['OrganisationDatasetrevisionLocalities']] = relationship('OrganisationDatasetrevisionLocalities', back_populates='datasetrevision')
    organisation_consumerfeedback: Mapped[List['OrganisationConsumerfeedback']] = relationship('OrganisationConsumerfeedback', back_populates='revision')


class OtcInactiveservice(Base):
    __tablename__ = 'otc_inactiveservice'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    registration_number: Mapped[str] = mapped_column(String(20))
    registration_status: Mapped[str] = mapped_column(String(20))
    effective_date: Mapped[Optional[datetime.date]] = mapped_column(Date)


class OtcLicence(Base):
    __tablename__ = 'otc_licence'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(9))
    status: Mapped[str] = mapped_column(String(30))
    granted_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    expiry_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    otc_service: Mapped[List['OtcService']] = relationship('OtcService', back_populates='licence')


class OtcOperator(Base):
    __tablename__ = 'otc_operator'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    operator_id: Mapped[int] = mapped_column(Integer)
    operator_name: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(Text)
    discs_in_possession: Mapped[Optional[int]] = mapped_column(Integer)
    authdiscs: Mapped[Optional[int]] = mapped_column(Integer)

    otc_service: Mapped[List['OtcService']] = relationship('OtcService', back_populates='operator')


class PipelinesBulkdataarchive(Base):
    __tablename__ = 'pipelines_bulkdataarchive'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    data: Mapped[str] = mapped_column(String(100))
    dataset_type: Mapped[int] = mapped_column(Integer)
    compliant_archive: Mapped[bool] = mapped_column(Boolean)
    traveline_regions: Mapped[str] = mapped_column(String(4))


class PipelinesChangedataarchive(Base):
    __tablename__ = 'pipelines_changedataarchive'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    published_at: Mapped[datetime.date] = mapped_column(Date)
    data: Mapped[str] = mapped_column(String(100))


class PipelinesPipelineerrorcode(Base):
    __tablename__ = 'pipelines_pipelineerrorcode'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    error: Mapped[str] = mapped_column(String(255))

    pipelines_fileprocessingresult: Mapped[List['PipelinesFileprocessingresult']] = relationship('PipelinesFileprocessingresult', back_populates='pipeline_error_code')


class PipelinesPipelineprocessingstep(Base):
    __tablename__ = 'pipelines_pipelineprocessingstep'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(20))

    pipelines_fileprocessingresult: Mapped[List['PipelinesFileprocessingresult']] = relationship('PipelinesFileprocessingresult', back_populates='pipeline_processing_step')


class PipelinesSchemadefinition(Base):
    __tablename__ = 'pipelines_schemadefinition'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    category: Mapped[str] = mapped_column(String(6))
    checksum: Mapped[str] = mapped_column(String(40))
    schema: Mapped[str] = mapped_column(String(100))


class SiteAdminDocumentarchive(Base):
    __tablename__ = 'site_admin_documentarchive'

    id: Mapped[int] = mapped_column(Integer, Sequence('site_admin_operationalmetricsarchive_id_seq'), primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    archive: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(50))


class SiteAdminMetricsarchive(Base):
    __tablename__ = 'site_admin_metricsarchive'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start: Mapped[datetime.date] = mapped_column(Date)
    end: Mapped[datetime.date] = mapped_column(Date)
    archive: Mapped[str] = mapped_column(String(100))


class SiteAdminOperationalstats(Base):
    __tablename__ = 'site_admin_operationalstats'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date)
    operator_count: Mapped[int] = mapped_column(Integer)
    operator_user_count: Mapped[int] = mapped_column(Integer)
    agent_user_count: Mapped[int] = mapped_column(Integer)
    consumer_count: Mapped[int] = mapped_column(Integer)
    timetables_count: Mapped[int] = mapped_column(Integer)
    avl_count: Mapped[int] = mapped_column(Integer)
    fares_count: Mapped[int] = mapped_column(Integer)
    published_timetable_operator_count: Mapped[int] = mapped_column(Integer)
    published_avl_operator_count: Mapped[int] = mapped_column(Integer)
    published_fares_operator_count: Mapped[int] = mapped_column(Integer)
    vehicle_count: Mapped[int] = mapped_column(Integer)
    registered_service_code_count: Mapped[Optional[int]] = mapped_column(Integer)
    unregistered_service_code_count: Mapped[Optional[int]] = mapped_column(Integer)


class SpatialRefSys(Base):
    __tablename__ = 'spatial_ref_sys'

    srid: Mapped[int] = mapped_column(Integer, primary_key=True)
    auth_name: Mapped[Optional[str]] = mapped_column(String(256))
    auth_srid: Mapped[Optional[int]] = mapped_column(Integer)
    srtext: Mapped[Optional[str]] = mapped_column(String(2048))
    proj4text: Mapped[Optional[str]] = mapped_column(String(2048))


class TransmodelBankholidays(Base):
    __tablename__ = 'transmodel_bankholidays'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    txc_element: Mapped[str] = mapped_column(String(255))
    date: Mapped[datetime.date] = mapped_column(Date)
    title: Mapped[Optional[str]] = mapped_column(String(255))
    notes: Mapped[Optional[str]] = mapped_column(String(255))
    division: Mapped[Optional[str]] = mapped_column(String(255))


class TransmodelServicedorganisations(Base):
    __tablename__ = 'transmodel_servicedorganisations'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    organisation_code: Mapped[Optional[str]] = mapped_column(String(255))

    transmodel_servicedorganisationvehiclejourney: Mapped[List['TransmodelServicedorganisationvehiclejourney']] = relationship('TransmodelServicedorganisationvehiclejourney', back_populates='serviced_organisation')


class TransmodelServicelink(Base):
    __tablename__ = 'transmodel_servicelink'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    from_stop_atco: Mapped[str] = mapped_column(String(255))
    to_stop_atco: Mapped[str] = mapped_column(String(255))
    from_stop_id: Mapped[Optional[int]] = mapped_column(Integer)
    to_stop_id: Mapped[Optional[int]] = mapped_column(Integer)

    transmodel_servicepattern_service_links: Mapped[List['TransmodelServicepatternServiceLinks']] = relationship('TransmodelServicepatternServiceLinks', back_populates='servicelink')


class TransmodelStopactivity(Base):
    __tablename__ = 'transmodel_stopactivity'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    is_pickup: Mapped[bool] = mapped_column(Boolean)
    is_setdown: Mapped[bool] = mapped_column(Boolean)
    is_driverrequest: Mapped[bool] = mapped_column(Boolean)

    transmodel_servicepatternstop: Mapped[List['TransmodelServicepatternstop']] = relationship('TransmodelServicepatternstop', back_populates='stop_activity')


class TransmodelTracks(Base):
    __tablename__ = 'transmodel_tracks'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    from_atco_code: Mapped[str] = mapped_column(String(255))
    to_atco_code: Mapped[str] = mapped_column(String(255))
    geometry: Mapped[Optional[Any]] = mapped_column(Geometry('LINESTRING', 4326, from_text='ST_GeomFromEWKT', name='geometry'))
    distance: Mapped[Optional[int]] = mapped_column(Integer)

    transmodel_tracksvehiclejourney: Mapped[List['TransmodelTracksvehiclejourney']] = relationship('TransmodelTracksvehiclejourney', back_populates='tracks')


class UiLta(Base):
    __tablename__ = 'ui_lta'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    avl_sra: Mapped[Optional[int]] = mapped_column(Integer)
    fares_sra: Mapped[Optional[int]] = mapped_column(Integer)
    overall_sra: Mapped[Optional[int]] = mapped_column(Integer)
    timetable_sra: Mapped[Optional[int]] = mapped_column(Integer)
    total_inscope: Mapped[Optional[int]] = mapped_column(Integer)

    naptan_adminarea: Mapped[List['NaptanAdminarea']] = relationship('NaptanAdminarea', back_populates='ui_lta')
    otc_localauthority: Mapped[List['OtcLocalauthority']] = relationship('OtcLocalauthority', back_populates='ui_lta')


class UsersUser(Base):
    __tablename__ = 'users_user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(128))
    is_superuser: Mapped[bool] = mapped_column(Boolean)
    username: Mapped[str] = mapped_column(String(150))
    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    is_staff: Mapped[bool] = mapped_column(Boolean)
    is_active: Mapped[bool] = mapped_column(Boolean)
    date_joined: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    account_type: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(254))
    description: Mapped[str] = mapped_column(String(400))
    dev_organisation: Mapped[str] = mapped_column(String(60))
    agent_organisation: Mapped[str] = mapped_column(String(60))
    notes: Mapped[str] = mapped_column(String(150))
    last_login: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    organisation_dataset: Mapped[List['OrganisationDataset']] = relationship('OrganisationDataset', back_populates='contact')
    organisation_datasetrevision: Mapped[List['OrganisationDatasetrevision']] = relationship('OrganisationDatasetrevision', back_populates='last_modified_user')
    organisation_datasetrevision_: Mapped[List['OrganisationDatasetrevision']] = relationship('OrganisationDatasetrevision', back_populates='published_by')
    account_emailaddress: Mapped[List['AccountEmailaddress']] = relationship('AccountEmailaddress', back_populates='user')
    authtoken_token: Mapped[List['AuthtokenToken']] = relationship('AuthtokenToken', back_populates='user')
    django_admin_log: Mapped[List['DjangoAdminLog']] = relationship('DjangoAdminLog', back_populates='user')
    invitations_invitation: Mapped[List['InvitationsInvitation']] = relationship('InvitationsInvitation', back_populates='inviter')
    organisation_datasetsubscription: Mapped[List['OrganisationDatasetsubscription']] = relationship('OrganisationDatasetsubscription', back_populates='user')
    organisation_organisation: Mapped[List['OrganisationOrganisation']] = relationship('OrganisationOrganisation', back_populates='key_contact')
    restrict_sessions_loggedinuser: Mapped[List['RestrictSessionsLoggedinuser']] = relationship('RestrictSessionsLoggedinuser', back_populates='user')
    site_admin_apirequest: Mapped[List['SiteAdminApirequest']] = relationship('SiteAdminApirequest', back_populates='requestor')
    site_admin_resourcerequestcounter: Mapped[List['SiteAdminResourcerequestcounter']] = relationship('SiteAdminResourcerequestcounter', back_populates='requestor')
    users_user_groups: Mapped[List['UsersUserGroups']] = relationship('UsersUserGroups', back_populates='user')
    waffle_flag_users: Mapped[List['WaffleFlagUsers']] = relationship('WaffleFlagUsers', back_populates='user')
    users_user_organisations: Mapped[List['UsersUserOrganisations']] = relationship('UsersUserOrganisations', back_populates='user')
    users_user_user_permissions: Mapped[List['UsersUserUserPermissions']] = relationship('UsersUserUserPermissions', back_populates='user')
    organisation_servicecodeexemption: Mapped[List['OrganisationServicecodeexemption']] = relationship('OrganisationServicecodeexemption', back_populates='exempted_by')
    users_agentuserinvite: Mapped[List['UsersAgentuserinvite']] = relationship('UsersAgentuserinvite', back_populates='agent')
    users_agentuserinvite_: Mapped[List['UsersAgentuserinvite']] = relationship('UsersAgentuserinvite', back_populates='inviter')
    organisation_consumerfeedback: Mapped[List['OrganisationConsumerfeedback']] = relationship('OrganisationConsumerfeedback', back_populates='consumer')


class WaffleFlag(Base):
    __tablename__ = 'waffle_flag'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    testing: Mapped[bool] = mapped_column(Boolean)
    superusers: Mapped[bool] = mapped_column(Boolean)
    staff: Mapped[bool] = mapped_column(Boolean)
    authenticated: Mapped[bool] = mapped_column(Boolean)
    languages: Mapped[str] = mapped_column(Text)
    rollout: Mapped[bool] = mapped_column(Boolean)
    note: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    everyone: Mapped[Optional[bool]] = mapped_column(Boolean)
    percent: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(3, 1))

    waffle_flag_groups: Mapped[List['WaffleFlagGroups']] = relationship('WaffleFlagGroups', back_populates='flag')
    waffle_flag_users: Mapped[List['WaffleFlagUsers']] = relationship('WaffleFlagUsers', back_populates='flag')


class WaffleSample(Base):
    __tablename__ = 'waffle_sample'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    percent: Mapped[decimal.Decimal] = mapped_column(Numeric(4, 1))
    note: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))


class WaffleSwitch(Base):
    __tablename__ = 'waffle_switch'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    active: Mapped[bool] = mapped_column(Boolean)
    note: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))


class AccountEmailaddress(Base):
    __tablename__ = 'account_emailaddress'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(254))
    verified: Mapped[bool] = mapped_column(Boolean)
    primary: Mapped[bool] = mapped_column(Boolean)
    user_id: Mapped[int] = mapped_column(Integer)

    user: Mapped['UsersUser'] = relationship('UsersUser', back_populates='account_emailaddress')
    account_emailconfirmation: Mapped[List['AccountEmailconfirmation']] = relationship('AccountEmailconfirmation', back_populates='email_address')


class AuthPermission(Base):
    __tablename__ = 'auth_permission'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    content_type_id: Mapped[int] = mapped_column(Integer)
    codename: Mapped[str] = mapped_column(String(100))

    content_type: Mapped['DjangoContentType'] = relationship('DjangoContentType', back_populates='auth_permission')
    auth_group_permissions: Mapped[List['AuthGroupPermissions']] = relationship('AuthGroupPermissions', back_populates='permission')
    users_user_user_permissions: Mapped[List['UsersUserUserPermissions']] = relationship('UsersUserUserPermissions', back_populates='permission')


class AuthtokenToken(Base):
    __tablename__ = 'authtoken_token'

    key: Mapped[str] = mapped_column(String(40), primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    user_id: Mapped[int] = mapped_column(Integer)

    user: Mapped['UsersUser'] = relationship('UsersUser', back_populates='authtoken_token')


class AvlAvlvalidationreport(Base):
    __tablename__ = 'avl_avlvalidationreport'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    critical_count: Mapped[int] = mapped_column(Integer)
    non_critical_count: Mapped[int] = mapped_column(Integer)
    created: Mapped[datetime.date] = mapped_column(Date)
    revision_id: Mapped[int] = mapped_column(Integer)
    critical_score: Mapped[float] = mapped_column(Double(53))
    non_critical_score: Mapped[float] = mapped_column(Double(53))
    vehicle_activity_count: Mapped[int] = mapped_column(Integer)
    file: Mapped[Optional[str]] = mapped_column(String(100))

    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='avl_avlvalidationreport')


class AvlCavlvalidationtaskresult(Base):
    __tablename__ = 'avl_cavlvalidationtaskresult'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    task_id: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50))
    revision_id: Mapped[int] = mapped_column(Integer)
    result: Mapped[str] = mapped_column(String(50))
    completed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='avl_cavlvalidationtaskresult')


class AvlPostpublishingcheckreport(Base):
    __tablename__ = 'avl_postpublishingcheckreport'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.date] = mapped_column(Date)
    granularity: Mapped[str] = mapped_column(String(6))
    file: Mapped[str] = mapped_column(String(100))
    dataset_id: Mapped[int] = mapped_column(Integer)
    vehicle_activities_analysed: Mapped[Optional[int]] = mapped_column(Integer)
    vehicle_activities_completely_matching: Mapped[Optional[int]] = mapped_column(Integer)

    dataset: Mapped['OrganisationDataset'] = relationship('OrganisationDataset', back_populates='avl_postpublishingcheckreport')


class DataQualityDataqualityreport(Base):
    __tablename__ = 'data_quality_dataqualityreport'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    file: Mapped[str] = mapped_column(String(100))
    revision_id: Mapped[int] = mapped_column(Integer)
    score: Mapped[float] = mapped_column(Double(53))

    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='data_quality_dataqualityreport')
    data_quality_dataqualityreportsummary: Mapped[List['DataQualityDataqualityreportsummary']] = relationship('DataQualityDataqualityreportsummary', back_populates='report')
    data_quality_fastlinkwarning: Mapped[List['DataQualityFastlinkwarning']] = relationship('DataQualityFastlinkwarning', back_populates='report')
    data_quality_fasttimingwarning: Mapped[List['DataQualityFasttimingwarning']] = relationship('DataQualityFasttimingwarning', back_populates='report')
    data_quality_incorrectnocwarning: Mapped[List['DataQualityIncorrectnocwarning']] = relationship('DataQualityIncorrectnocwarning', back_populates='report')
    data_quality_journeyconflictwarning: Mapped[List['DataQualityJourneyconflictwarning']] = relationship('DataQualityJourneyconflictwarning', back_populates='report')
    data_quality_journeydaterangebackwardswarning: Mapped[List['DataQualityJourneydaterangebackwardswarning']] = relationship('DataQualityJourneydaterangebackwardswarning', back_populates='report')
    data_quality_journeyduplicatewarning: Mapped[List['DataQualityJourneyduplicatewarning']] = relationship('DataQualityJourneyduplicatewarning', back_populates='report')
    data_quality_journeystopinappropriatewarning: Mapped[List['DataQualityJourneystopinappropriatewarning']] = relationship('DataQualityJourneystopinappropriatewarning', back_populates='report')
    data_quality_journeywithoutheadsignwarning: Mapped[List['DataQualityJourneywithoutheadsignwarning']] = relationship('DataQualityJourneywithoutheadsignwarning', back_populates='report')
    data_quality_lineexpiredwarning: Mapped[List['DataQualityLineexpiredwarning']] = relationship('DataQualityLineexpiredwarning', back_populates='report')
    data_quality_linemissingblockidwarning: Mapped[List['DataQualityLinemissingblockidwarning']] = relationship('DataQualityLinemissingblockidwarning', back_populates='report')
    data_quality_service_reports: Mapped[List['DataQualityServiceReports']] = relationship('DataQualityServiceReports', back_populates='dataqualityreport')
    data_quality_servicelinkmissingstopwarning: Mapped[List['DataQualityServicelinkmissingstopwarning']] = relationship('DataQualityServicelinkmissingstopwarning', back_populates='report')
    data_quality_slowlinkwarning: Mapped[List['DataQualitySlowlinkwarning']] = relationship('DataQualitySlowlinkwarning', back_populates='report')
    data_quality_slowtimingwarning: Mapped[List['DataQualitySlowtimingwarning']] = relationship('DataQualitySlowtimingwarning', back_populates='report')
    data_quality_stopincorrecttypewarning: Mapped[List['DataQualityStopincorrecttypewarning']] = relationship('DataQualityStopincorrecttypewarning', back_populates='report')
    data_quality_stopmissingnaptanwarning: Mapped[List['DataQualityStopmissingnaptanwarning']] = relationship('DataQualityStopmissingnaptanwarning', back_populates='report')
    data_quality_timingbackwardswarning: Mapped[List['DataQualityTimingbackwardswarning']] = relationship('DataQualityTimingbackwardswarning', back_populates='report')
    data_quality_timingdropoffwarning: Mapped[List['DataQualityTimingdropoffwarning']] = relationship('DataQualityTimingdropoffwarning', back_populates='report')
    data_quality_timingfirstwarning: Mapped[List['DataQualityTimingfirstwarning']] = relationship('DataQualityTimingfirstwarning', back_populates='report')
    data_quality_timinglastwarning: Mapped[List['DataQualityTiminglastwarning']] = relationship('DataQualityTiminglastwarning', back_populates='report')
    data_quality_timingmissingpointwarning: Mapped[List['DataQualityTimingmissingpointwarning']] = relationship('DataQualityTimingmissingpointwarning', back_populates='report')
    data_quality_timingmultiplewarning: Mapped[List['DataQualityTimingmultiplewarning']] = relationship('DataQualityTimingmultiplewarning', back_populates='report')
    data_quality_timingpickupwarning: Mapped[List['DataQualityTimingpickupwarning']] = relationship('DataQualityTimingpickupwarning', back_populates='report')
    pipelines_dataqualitytask: Mapped[List['PipelinesDataqualitytask']] = relationship('PipelinesDataqualitytask', back_populates='report')


class DataQualityPostschemaviolation(Base):
    __tablename__ = 'data_quality_postschemaviolation'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(256))
    details: Mapped[str] = mapped_column(String(1024))
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    revision_id: Mapped[int] = mapped_column(Integer)
    additional_details: Mapped[Optional[dict]] = mapped_column(JSONB)

    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='data_quality_postschemaviolation')


class DataQualityPtiobservation(Base):
    __tablename__ = 'data_quality_ptiobservation'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(256))
    line: Mapped[int] = mapped_column(Integer)
    details: Mapped[str] = mapped_column(String(1024))
    element: Mapped[str] = mapped_column(String(256))
    category: Mapped[str] = mapped_column(String(1024))
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    revision_id: Mapped[int] = mapped_column(Integer)
    reference: Mapped[str] = mapped_column(String(64))

    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='data_quality_ptiobservation')


class DataQualityPtivalidationresult(Base):
    __tablename__ = 'data_quality_ptivalidationresult'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    count: Mapped[int] = mapped_column(Integer)
    report: Mapped[str] = mapped_column(String(100))
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    revision_id: Mapped[int] = mapped_column(Integer)

    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='data_quality_ptivalidationresult')


class DataQualityReport(Base):
    __tablename__ = 'data_quality_report'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    file_name: Mapped[str] = mapped_column(String(255))
    revision_id: Mapped[int] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(String(64))

    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='data_quality_report')
    data_quality_taskresults: Mapped[List['DataQualityTaskresults']] = relationship('DataQualityTaskresults', back_populates='dataquality_report')


class DataQualitySchemaviolation(Base):
    __tablename__ = 'data_quality_schemaviolation'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(256))
    line: Mapped[int] = mapped_column(Integer)
    details: Mapped[str] = mapped_column(String(1024))
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    revision_id: Mapped[int] = mapped_column(Integer)

    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='data_quality_schemaviolation')


class DataQualityTimingpatternstop(Base):
    __tablename__ = 'data_quality_timingpatternstop'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    arrival: Mapped[datetime.timedelta] = mapped_column(INTERVAL)
    departure: Mapped[datetime.timedelta] = mapped_column(INTERVAL)
    pickup_allowed: Mapped[bool] = mapped_column(Boolean)
    setdown_allowed: Mapped[bool] = mapped_column(Boolean)
    timing_point: Mapped[bool] = mapped_column(Boolean)
    service_pattern_stop_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    service_pattern_stop: Mapped['DataQualityServicepatternstop'] = relationship('DataQualityServicepatternstop', back_populates='data_quality_timingpatternstop')
    timing_pattern: Mapped['DataQualityTimingpattern'] = relationship('DataQualityTimingpattern', back_populates='data_quality_timingpatternstop')
    data_quality_timingbackwardswarning: Mapped[List['DataQualityTimingbackwardswarning']] = relationship('DataQualityTimingbackwardswarning', back_populates='from_stop')
    data_quality_timingbackwardswarning_: Mapped[List['DataQualityTimingbackwardswarning']] = relationship('DataQualityTimingbackwardswarning', back_populates='to_stop')
    data_quality_fastlinkwarning_timings: Mapped[List['DataQualityFastlinkwarningTimings']] = relationship('DataQualityFastlinkwarningTimings', back_populates='timingpatternstop')
    data_quality_fasttimingwarning_timings: Mapped[List['DataQualityFasttimingwarningTimings']] = relationship('DataQualityFasttimingwarningTimings', back_populates='timingpatternstop')
    data_quality_slowlinkwarning_timings: Mapped[List['DataQualitySlowlinkwarningTimings']] = relationship('DataQualitySlowlinkwarningTimings', back_populates='timingpatternstop')
    data_quality_slowtimingwarning_timings: Mapped[List['DataQualitySlowtimingwarningTimings']] = relationship('DataQualitySlowtimingwarningTimings', back_populates='timingpatternstop')
    data_quality_timingbackwardswarning_timings: Mapped[List['DataQualityTimingbackwardswarningTimings']] = relationship('DataQualityTimingbackwardswarningTimings', back_populates='timingpatternstop')
    data_quality_timingdropoffwarning_timings: Mapped[List['DataQualityTimingdropoffwarningTimings']] = relationship('DataQualityTimingdropoffwarningTimings', back_populates='timingpatternstop')
    data_quality_timingfirstwarning_timings: Mapped[List['DataQualityTimingfirstwarningTimings']] = relationship('DataQualityTimingfirstwarningTimings', back_populates='timingpatternstop')
    data_quality_timinglastwarning_timings: Mapped[List['DataQualityTiminglastwarningTimings']] = relationship('DataQualityTiminglastwarningTimings', back_populates='timingpatternstop')
    data_quality_timingmissingpointwarning_timings: Mapped[List['DataQualityTimingmissingpointwarningTimings']] = relationship('DataQualityTimingmissingpointwarningTimings', back_populates='timingpatternstop')
    data_quality_timingmultiplewarning_timings: Mapped[List['DataQualityTimingmultiplewarningTimings']] = relationship('DataQualityTimingmultiplewarningTimings', back_populates='timingpatternstop')
    data_quality_timingpickupwarning_timings: Mapped[List['DataQualityTimingpickupwarningTimings']] = relationship('DataQualityTimingpickupwarningTimings', back_populates='timingpatternstop')


class DataQualityVehiclejourney(Base):
    __tablename__ = 'data_quality_vehiclejourney'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[datetime.time] = mapped_column(Time)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)
    ito_id: Mapped[str] = mapped_column(Text)
    dates: Mapped[list] = mapped_column(ARRAY(Date()))

    timing_pattern: Mapped['DataQualityTimingpattern'] = relationship('DataQualityTimingpattern', back_populates='data_quality_vehiclejourney')
    data_quality_journeyconflictwarning: Mapped[List['DataQualityJourneyconflictwarning']] = relationship('DataQualityJourneyconflictwarning', back_populates='conflict')
    data_quality_journeyconflictwarning_: Mapped[List['DataQualityJourneyconflictwarning']] = relationship('DataQualityJourneyconflictwarning', back_populates='vehicle_journey')
    data_quality_journeydaterangebackwardswarning: Mapped[List['DataQualityJourneydaterangebackwardswarning']] = relationship('DataQualityJourneydaterangebackwardswarning', back_populates='vehicle_journey')
    data_quality_journeyduplicatewarning: Mapped[List['DataQualityJourneyduplicatewarning']] = relationship('DataQualityJourneyduplicatewarning', back_populates='duplicate')
    data_quality_journeyduplicatewarning_: Mapped[List['DataQualityJourneyduplicatewarning']] = relationship('DataQualityJourneyduplicatewarning', back_populates='vehicle_journey')
    data_quality_journeywithoutheadsignwarning: Mapped[List['DataQualityJourneywithoutheadsignwarning']] = relationship('DataQualityJourneywithoutheadsignwarning', back_populates='vehicle_journey')
    data_quality_journeystopinappropriatewarning_vehicle_journeys: Mapped[List['DataQualityJourneystopinappropriatewarningVehicleJourneys']] = relationship('DataQualityJourneystopinappropriatewarningVehicleJourneys', back_populates='vehiclejourney')
    data_quality_lineexpiredwarning_vehicle_journeys: Mapped[List['DataQualityLineexpiredwarningVehicleJourneys']] = relationship('DataQualityLineexpiredwarningVehicleJourneys', back_populates='vehiclejourney')
    data_quality_linemissingblockidwarning_vehicle_journeys: Mapped[List['DataQualityLinemissingblockidwarningVehicleJourneys']] = relationship('DataQualityLinemissingblockidwarningVehicleJourneys', back_populates='vehiclejourney')


class DjangoAdminLog(Base):
    __tablename__ = 'django_admin_log'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action_time: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    object_repr: Mapped[str] = mapped_column(String(200))
    action_flag: Mapped[int] = mapped_column(SmallInteger)
    change_message: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(Integer)
    object_id: Mapped[Optional[str]] = mapped_column(Text)
    content_type_id: Mapped[Optional[int]] = mapped_column(Integer)

    content_type: Mapped[Optional['DjangoContentType']] = relationship('DjangoContentType', back_populates='django_admin_log')
    user: Mapped['UsersUser'] = relationship('UsersUser', back_populates='django_admin_log')


class DjangoCeleryBeatPeriodictask(Base):
    __tablename__ = 'django_celery_beat_periodictask'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    task: Mapped[str] = mapped_column(String(200))
    args: Mapped[str] = mapped_column(Text)
    kwargs: Mapped[str] = mapped_column(Text)
    enabled: Mapped[bool] = mapped_column(Boolean)
    total_run_count: Mapped[int] = mapped_column(Integer)
    date_changed: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    description: Mapped[str] = mapped_column(Text)
    one_off: Mapped[bool] = mapped_column(Boolean)
    headers: Mapped[str] = mapped_column(Text)
    queue: Mapped[Optional[str]] = mapped_column(String(200))
    exchange: Mapped[Optional[str]] = mapped_column(String(200))
    routing_key: Mapped[Optional[str]] = mapped_column(String(200))
    expires: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    last_run_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    crontab_id: Mapped[Optional[int]] = mapped_column(Integer)
    interval_id: Mapped[Optional[int]] = mapped_column(Integer)
    solar_id: Mapped[Optional[int]] = mapped_column(Integer)
    start_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    priority: Mapped[Optional[int]] = mapped_column(Integer)
    clocked_id: Mapped[Optional[int]] = mapped_column(Integer)
    expire_seconds: Mapped[Optional[int]] = mapped_column(Integer)

    clocked: Mapped[Optional['DjangoCeleryBeatClockedschedule']] = relationship('DjangoCeleryBeatClockedschedule', back_populates='django_celery_beat_periodictask')
    crontab: Mapped[Optional['DjangoCeleryBeatCrontabschedule']] = relationship('DjangoCeleryBeatCrontabschedule', back_populates='django_celery_beat_periodictask')
    interval: Mapped[Optional['DjangoCeleryBeatIntervalschedule']] = relationship('DjangoCeleryBeatIntervalschedule', back_populates='django_celery_beat_periodictask')
    solar: Mapped[Optional['DjangoCeleryBeatSolarschedule']] = relationship('DjangoCeleryBeatSolarschedule', back_populates='django_celery_beat_periodictask')


class DqsReport(Base):
    __tablename__ = 'dqs_report'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    file_name: Mapped[str] = mapped_column(String(255))
    revision_id: Mapped[int] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(String(64))

    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='dqs_report')
    dqs_taskresults: Mapped[List['DqsTaskresults']] = relationship('DqsTaskresults', back_populates='dataquality_report')


class InvitationsInvitation(Base):
    __tablename__ = 'invitations_invitation'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(String(254))
    accepted: Mapped[bool] = mapped_column(Boolean)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    key: Mapped[str] = mapped_column(String(64))
    sent: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    inviter_id: Mapped[Optional[int]] = mapped_column(Integer)

    inviter: Mapped[Optional['UsersUser']] = relationship('UsersUser', back_populates='invitations_invitation')


class NaptanAdminarea(Base):
    __tablename__ = 'naptan_adminarea'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    traveline_region_id: Mapped[str] = mapped_column(String(255))
    atco_code: Mapped[str] = mapped_column(String(255))
    ui_lta_id: Mapped[Optional[int]] = mapped_column(Integer)

    ui_lta: Mapped[Optional['UiLta']] = relationship('UiLta', back_populates='naptan_adminarea')
    naptan_locality: Mapped[List['NaptanLocality']] = relationship('NaptanLocality', back_populates='admin_area')
    organisation_datasetrevision_admin_areas: Mapped[List['OrganisationDatasetrevisionAdminAreas']] = relationship('OrganisationDatasetrevisionAdminAreas', back_populates='adminarea')
    organisation_organisation_admin_areas: Mapped[List['OrganisationOrganisationAdminAreas']] = relationship('OrganisationOrganisationAdminAreas', back_populates='adminarea')
    transmodel_servicepattern_admin_areas: Mapped[List['TransmodelServicepatternAdminAreas']] = relationship('TransmodelServicepatternAdminAreas', back_populates='adminarea')
    naptan_stoppoint: Mapped[List['NaptanStoppoint']] = relationship('NaptanStoppoint', back_populates='admin_area')


class OrganisationAvlcompliancecache(Base):
    __tablename__ = 'organisation_avlcompliancecache'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String(50))
    dataset_id: Mapped[int] = mapped_column(Integer)

    dataset: Mapped['OrganisationDataset'] = relationship('OrganisationDataset', back_populates='organisation_avlcompliancecache')


class OrganisationDatasetmetadata(Base):
    __tablename__ = 'organisation_datasetmetadata'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    schema_version: Mapped[str] = mapped_column(String(8))
    revision_id: Mapped[int] = mapped_column(Integer)

    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='organisation_datasetmetadata')


class OrganisationDatasetsubscription(Base):
    __tablename__ = 'organisation_datasetsubscription'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    dataset_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)

    dataset: Mapped['OrganisationDataset'] = relationship('OrganisationDataset', back_populates='organisation_datasetsubscription')
    user: Mapped['UsersUser'] = relationship('UsersUser', back_populates='organisation_datasetsubscription')


class OrganisationOrganisation(Base):
    __tablename__ = 'organisation_organisation'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    name: Mapped[str] = mapped_column(String(255))
    short_name: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean)
    is_abods_global_viewer: Mapped[bool] = mapped_column(Boolean)
    key_contact_id: Mapped[Optional[int]] = mapped_column(Integer)
    licence_required: Mapped[Optional[bool]] = mapped_column(Boolean)
    avl_sra: Mapped[Optional[int]] = mapped_column(Integer)
    fares_sra: Mapped[Optional[int]] = mapped_column(Integer)
    overall_sra: Mapped[Optional[int]] = mapped_column(Integer)
    timetable_sra: Mapped[Optional[int]] = mapped_column(Integer)
    total_inscope: Mapped[Optional[int]] = mapped_column(Integer)

    organisation_dataset: Mapped[List['OrganisationDataset']] = relationship('OrganisationDataset', back_populates='organisation')
    key_contact: Mapped[Optional['UsersUser']] = relationship('UsersUser', back_populates='organisation_organisation')
    fares_validator_faresvalidation: Mapped[List['FaresValidatorFaresvalidation']] = relationship('FaresValidatorFaresvalidation', back_populates='organisation')
    fares_validator_faresvalidationresult: Mapped[List['FaresValidatorFaresvalidationresult']] = relationship('FaresValidatorFaresvalidationresult', back_populates='organisation')
    organisation_consumerstats: Mapped[List['OrganisationConsumerstats']] = relationship('OrganisationConsumerstats', back_populates='organisation')
    organisation_licence: Mapped[List['OrganisationLicence']] = relationship('OrganisationLicence', back_populates='organisation')
    organisation_operatorcode: Mapped[List['OrganisationOperatorcode']] = relationship('OrganisationOperatorcode', back_populates='organisation')
    organisation_organisation_admin_areas: Mapped[List['OrganisationOrganisationAdminAreas']] = relationship('OrganisationOrganisationAdminAreas', back_populates='organisation')
    users_invitation: Mapped[List['UsersInvitation']] = relationship('UsersInvitation', back_populates='organisation')
    users_user_organisations: Mapped[List['UsersUserOrganisations']] = relationship('UsersUserOrganisations', back_populates='organisation')
    users_agentuserinvite: Mapped[List['UsersAgentuserinvite']] = relationship('UsersAgentuserinvite', back_populates='organisation')
    organisation_consumerfeedback: Mapped[List['OrganisationConsumerfeedback']] = relationship('OrganisationConsumerfeedback', back_populates='organisation')


class OrganisationTxcfileattributes(Base):
    __tablename__ = 'organisation_txcfileattributes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    schema_version: Mapped[str] = mapped_column(String(10))
    revision_number: Mapped[int] = mapped_column(Integer)
    creation_datetime: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modification_datetime: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    filename: Mapped[str] = mapped_column(String(512))
    service_code: Mapped[str] = mapped_column(String(100))
    revision_id: Mapped[int] = mapped_column(Integer)
    modification: Mapped[str] = mapped_column(String(28))
    national_operator_code: Mapped[str] = mapped_column(String(100))
    licence_number: Mapped[str] = mapped_column(String(56))
    public_use: Mapped[bool] = mapped_column(Boolean)
    line_names: Mapped[list] = mapped_column(ARRAY(String(length=255)))
    destination: Mapped[str] = mapped_column(String(512))
    origin: Mapped[str] = mapped_column(String(512))
    hash: Mapped[str] = mapped_column(String(40))
    service_mode: Mapped[str] = mapped_column(String(20))
    operating_period_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    operating_period_start_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='organisation_txcfileattributes')
    data_quality_taskresults: Mapped[List['DataQualityTaskresults']] = relationship('DataQualityTaskresults', back_populates='transmodel_txcfileattributes')
    dqs_taskresults: Mapped[List['DqsTaskresults']] = relationship('DqsTaskresults', back_populates='transmodel_txcfileattributes')
    transmodel_service: Mapped[List['TransmodelService']] = relationship('TransmodelService', back_populates='txcfileattributes')


class OtcLocalauthority(Base):
    __tablename__ = 'otc_localauthority'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    ui_lta_id: Mapped[Optional[int]] = mapped_column(Integer)

    ui_lta: Mapped[Optional['UiLta']] = relationship('UiLta', back_populates='otc_localauthority')
    otc_localauthority_registration_numbers: Mapped[List['OtcLocalauthorityRegistrationNumbers']] = relationship('OtcLocalauthorityRegistrationNumbers', back_populates='localauthority')


class OtcService(Base):
    __tablename__ = 'otc_service'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    registration_number: Mapped[str] = mapped_column(String(25))
    variation_number: Mapped[int] = mapped_column(Integer)
    service_number: Mapped[str] = mapped_column(String(1000))
    current_traffic_area: Mapped[str] = mapped_column(String(1))
    start_point: Mapped[str] = mapped_column(Text)
    finish_point: Mapped[str] = mapped_column(Text)
    via: Mapped[str] = mapped_column(Text)
    service_type_other_details: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(String(25))
    registration_status: Mapped[str] = mapped_column(String(20))
    public_text: Mapped[str] = mapped_column(Text)
    service_type_description: Mapped[str] = mapped_column(String(1000))
    subsidies_description: Mapped[str] = mapped_column(String(7))
    subsidies_details: Mapped[str] = mapped_column(Text)
    effective_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    received_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    registration_code: Mapped[Optional[int]] = mapped_column(Integer)
    short_notice: Mapped[Optional[bool]] = mapped_column(Boolean)
    licence_id: Mapped[Optional[int]] = mapped_column(Integer)
    operator_id: Mapped[Optional[int]] = mapped_column(Integer)
    last_modified: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    api_type: Mapped[Optional[str]] = mapped_column(Text)
    atco_code: Mapped[Optional[str]] = mapped_column(Text)

    licence: Mapped[Optional['OtcLicence']] = relationship('OtcLicence', back_populates='otc_service')
    operator: Mapped[Optional['OtcOperator']] = relationship('OtcOperator', back_populates='otc_service')
    otc_localauthority_registration_numbers: Mapped[List['OtcLocalauthorityRegistrationNumbers']] = relationship('OtcLocalauthorityRegistrationNumbers', back_populates='service')


class PipelinesDatasetetlerror(Base):
    __tablename__ = 'pipelines_datasetetlerror'

    id: Mapped[int] = mapped_column(Integer, Sequence('pipelines_datasetetlerrors_id_seq'), primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    severity: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(8096))
    revision_id: Mapped[Optional[int]] = mapped_column(Integer)

    revision: Mapped[Optional['OrganisationDatasetrevision']] = relationship('OrganisationDatasetrevision', back_populates='pipelines_datasetetlerror')


class PipelinesDatasetetltaskresult(Base):
    __tablename__ = 'pipelines_datasetetltaskresult'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    progress: Mapped[int] = mapped_column(Integer)
    revision_id: Mapped[int] = mapped_column(Integer)
    error_code: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50))
    task_id: Mapped[str] = mapped_column(String(255))
    task_name_failed: Mapped[str] = mapped_column(String(255))
    completed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    additional_info: Mapped[Optional[str]] = mapped_column(String(512))

    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='pipelines_datasetetltaskresult')


class PipelinesFileprocessingresult(Base):
    __tablename__ = 'pipelines_fileprocessingresult'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    task_id: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50))
    filename: Mapped[str] = mapped_column(String(255))
    pipeline_processing_step_id: Mapped[int] = mapped_column(Integer)
    revision_id: Mapped[int] = mapped_column(Integer)
    completed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    pipeline_error_code_id: Mapped[Optional[int]] = mapped_column(Integer)

    pipeline_error_code: Mapped[Optional['PipelinesPipelineerrorcode']] = relationship('PipelinesPipelineerrorcode', back_populates='pipelines_fileprocessingresult')
    pipeline_processing_step: Mapped['PipelinesPipelineprocessingstep'] = relationship('PipelinesPipelineprocessingstep', back_populates='pipelines_fileprocessingresult')
    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='pipelines_fileprocessingresult')


class PipelinesRemotedatasethealthcheckcount(Base):
    __tablename__ = 'pipelines_remotedatasethealthcheckcount'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    count: Mapped[int] = mapped_column(Integer)
    revision_id: Mapped[int] = mapped_column(Integer)

    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='pipelines_remotedatasethealthcheckcount')


class RestrictSessionsLoggedinuser(Base):
    __tablename__ = 'restrict_sessions_loggedinuser'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    session_key: Mapped[Optional[str]] = mapped_column(String(32))

    user: Mapped['UsersUser'] = relationship('UsersUser', back_populates='restrict_sessions_loggedinuser')


class SiteAdminApirequest(Base):
    __tablename__ = 'site_admin_apirequest'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    path_info: Mapped[str] = mapped_column(String(512))
    query_string: Mapped[str] = mapped_column(String(512))
    requestor_id: Mapped[int] = mapped_column(Integer)

    requestor: Mapped['UsersUser'] = relationship('UsersUser', back_populates='site_admin_apirequest')


class SiteAdminResourcerequestcounter(Base):
    __tablename__ = 'site_admin_resourcerequestcounter'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date)
    path_info: Mapped[str] = mapped_column(String(512))
    counter: Mapped[int] = mapped_column(Integer)
    requestor_id: Mapped[Optional[int]] = mapped_column(Integer)

    requestor: Mapped[Optional['UsersUser']] = relationship('UsersUser', back_populates='site_admin_resourcerequestcounter')


class TransmodelServicepattern(Base):
    __tablename__ = 'transmodel_servicepattern'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_pattern_id: Mapped[str] = mapped_column(String(255))
    origin: Mapped[str] = mapped_column(String(255))
    destination: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    geom: Mapped[Optional[Any]] = mapped_column(Geometry('LINESTRING', 4326, from_text='ST_GeomFromEWKT', name='geometry'))
    revision_id: Mapped[Optional[int]] = mapped_column(Integer)
    line_name: Mapped[Optional[str]] = mapped_column(String(255))

    revision: Mapped[Optional['OrganisationDatasetrevision']] = relationship('OrganisationDatasetrevision', back_populates='transmodel_servicepattern')
    transmodel_vehiclejourney: Mapped[List['TransmodelVehiclejourney']] = relationship('TransmodelVehiclejourney', back_populates='service_pattern')
    organisation_consumerfeedback: Mapped[List['OrganisationConsumerfeedback']] = relationship('OrganisationConsumerfeedback', back_populates='service_pattern')


class TransmodelServicepatternServiceLinks(Base):
    __tablename__ = 'transmodel_servicepattern_service_links'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    servicepattern_id: Mapped[int] = mapped_column(Integer)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    servicelink: Mapped['TransmodelServicelink'] = relationship('TransmodelServicelink', back_populates='transmodel_servicepattern_service_links')


class UsersUserGroups(Base):
    __tablename__ = 'users_user_groups'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    group_id: Mapped[int] = mapped_column(Integer)

    group: Mapped['AuthGroup'] = relationship('AuthGroup', back_populates='users_user_groups')
    user: Mapped['UsersUser'] = relationship('UsersUser', back_populates='users_user_groups')


class UsersUsersettings(UsersUser):
    __tablename__ = 'users_usersettings'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mute_all_dataset_notifications: Mapped[bool] = mapped_column(Boolean)
    notify_invitation_accepted: Mapped[bool] = mapped_column(Boolean)
    opt_in_user_research: Mapped[bool] = mapped_column(Boolean)
    share_app_usage: Mapped[bool] = mapped_column(Boolean)
    notify_avl_unavailable: Mapped[bool] = mapped_column(Boolean)
    daily_compliance_check_alert: Mapped[bool] = mapped_column(Boolean)
    regional_areas: Mapped[str] = mapped_column(String(60))
    intended_use: Mapped[Optional[int]] = mapped_column(Integer)
    national_interest: Mapped[Optional[bool]] = mapped_column(Boolean)


class WaffleFlagGroups(Base):
    __tablename__ = 'waffle_flag_groups'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    flag_id: Mapped[int] = mapped_column(Integer)
    group_id: Mapped[int] = mapped_column(Integer)

    flag: Mapped['WaffleFlag'] = relationship('WaffleFlag', back_populates='waffle_flag_groups')
    group: Mapped['AuthGroup'] = relationship('AuthGroup', back_populates='waffle_flag_groups')


class WaffleFlagUsers(Base):
    __tablename__ = 'waffle_flag_users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    flag_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)

    flag: Mapped['WaffleFlag'] = relationship('WaffleFlag', back_populates='waffle_flag_users')
    user: Mapped['UsersUser'] = relationship('UsersUser', back_populates='waffle_flag_users')


class AccountEmailconfirmation(Base):
    __tablename__ = 'account_emailconfirmation'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    key: Mapped[str] = mapped_column(String(64))
    email_address_id: Mapped[int] = mapped_column(Integer)
    sent: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    email_address: Mapped['AccountEmailaddress'] = relationship('AccountEmailaddress', back_populates='account_emailconfirmation')


class AuthGroupPermissions(Base):
    __tablename__ = 'auth_group_permissions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer)
    permission_id: Mapped[int] = mapped_column(Integer)

    group: Mapped['AuthGroup'] = relationship('AuthGroup', back_populates='auth_group_permissions')
    permission: Mapped['AuthPermission'] = relationship('AuthPermission', back_populates='auth_group_permissions')


class DataQualityDataqualityreportsummary(Base):
    __tablename__ = 'data_quality_dataqualityreportsummary'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data: Mapped[dict] = mapped_column(JSONB)
    report_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_dataqualityreportsummary')


class DataQualityFastlinkwarning(Base):
    __tablename__ = 'data_quality_fastlinkwarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_fastlinkwarning')
    timing_pattern: Mapped['DataQualityTimingpattern'] = relationship('DataQualityTimingpattern', back_populates='data_quality_fastlinkwarning')
    data_quality_fastlinkwarning_service_links: Mapped[List['DataQualityFastlinkwarningServiceLinks']] = relationship('DataQualityFastlinkwarningServiceLinks', back_populates='fastlinkwarning')
    data_quality_fastlinkwarning_timings: Mapped[List['DataQualityFastlinkwarningTimings']] = relationship('DataQualityFastlinkwarningTimings', back_populates='fastlinkwarning')


class DataQualityFasttimingwarning(Base):
    __tablename__ = 'data_quality_fasttimingwarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_fasttimingwarning')
    timing_pattern: Mapped['DataQualityTimingpattern'] = relationship('DataQualityTimingpattern', back_populates='data_quality_fasttimingwarning')
    data_quality_fasttimingwarning_service_links: Mapped[List['DataQualityFasttimingwarningServiceLinks']] = relationship('DataQualityFasttimingwarningServiceLinks', back_populates='fasttimingwarning')
    data_quality_fasttimingwarning_timings: Mapped[List['DataQualityFasttimingwarningTimings']] = relationship('DataQualityFasttimingwarningTimings', back_populates='fasttimingwarning')


class DataQualityIncorrectnocwarning(Base):
    __tablename__ = 'data_quality_incorrectnocwarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    noc: Mapped[str] = mapped_column(Text)
    report_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_incorrectnocwarning')


class DataQualityJourneyconflictwarning(Base):
    __tablename__ = 'data_quality_journeyconflictwarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    conflict_id: Mapped[int] = mapped_column(Integer)
    report_id: Mapped[int] = mapped_column(Integer)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)

    conflict: Mapped['DataQualityVehiclejourney'] = relationship('DataQualityVehiclejourney', back_populates='data_quality_journeyconflictwarning')
    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_journeyconflictwarning')
    vehicle_journey: Mapped['DataQualityVehiclejourney'] = relationship('DataQualityVehiclejourney', back_populates='data_quality_journeyconflictwarning_')
    data_quality_journeyconflictwarning_stops: Mapped[List['DataQualityJourneyconflictwarningStops']] = relationship('DataQualityJourneyconflictwarningStops', back_populates='journeyconflictwarning')


class DataQualityJourneydaterangebackwardswarning(Base):
    __tablename__ = 'data_quality_journeydaterangebackwardswarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    start: Mapped[datetime.date] = mapped_column(Date)
    end: Mapped[datetime.date] = mapped_column(Date)
    report_id: Mapped[int] = mapped_column(Integer)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_journeydaterangebackwardswarning')
    vehicle_journey: Mapped['DataQualityVehiclejourney'] = relationship('DataQualityVehiclejourney', back_populates='data_quality_journeydaterangebackwardswarning')


class DataQualityJourneyduplicatewarning(Base):
    __tablename__ = 'data_quality_journeyduplicatewarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)
    duplicate_id: Mapped[int] = mapped_column(Integer)

    duplicate: Mapped['DataQualityVehiclejourney'] = relationship('DataQualityVehiclejourney', back_populates='data_quality_journeyduplicatewarning')
    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_journeyduplicatewarning')
    vehicle_journey: Mapped['DataQualityVehiclejourney'] = relationship('DataQualityVehiclejourney', back_populates='data_quality_journeyduplicatewarning_')


class DataQualityJourneystopinappropriatewarning(Base):
    __tablename__ = 'data_quality_journeystopinappropriatewarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    stop_type: Mapped[str] = mapped_column(Text)
    report_id: Mapped[int] = mapped_column(Integer)
    stop_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_journeystopinappropriatewarning')
    data_quality_journeystopinappropriatewarning_vehicle_journeys: Mapped[List['DataQualityJourneystopinappropriatewarningVehicleJourneys']] = relationship('DataQualityJourneystopinappropriatewarningVehicleJourneys', back_populates='journeystopinappropriatewarning')


class DataQualityJourneywithoutheadsignwarning(Base):
    __tablename__ = 'data_quality_journeywithoutheadsignwarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_journeywithoutheadsignwarning')
    vehicle_journey: Mapped['DataQualityVehiclejourney'] = relationship('DataQualityVehiclejourney', back_populates='data_quality_journeywithoutheadsignwarning')


class DataQualityLineexpiredwarning(Base):
    __tablename__ = 'data_quality_lineexpiredwarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    service_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_lineexpiredwarning')
    service: Mapped['DataQualityService'] = relationship('DataQualityService', back_populates='data_quality_lineexpiredwarning')
    data_quality_lineexpiredwarning_vehicle_journeys: Mapped[List['DataQualityLineexpiredwarningVehicleJourneys']] = relationship('DataQualityLineexpiredwarningVehicleJourneys', back_populates='lineexpiredwarning')


class DataQualityLinemissingblockidwarning(Base):
    __tablename__ = 'data_quality_linemissingblockidwarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    service_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_linemissingblockidwarning')
    service: Mapped['DataQualityService'] = relationship('DataQualityService', back_populates='data_quality_linemissingblockidwarning')
    data_quality_linemissingblockidwarning_vehicle_journeys: Mapped[List['DataQualityLinemissingblockidwarningVehicleJourneys']] = relationship('DataQualityLinemissingblockidwarningVehicleJourneys', back_populates='linemissingblockidwarning')


class DataQualityServiceReports(Base):
    __tablename__ = 'data_quality_service_reports'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_id: Mapped[int] = mapped_column(Integer)
    dataqualityreport_id: Mapped[int] = mapped_column(Integer)

    dataqualityreport: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_service_reports')
    service: Mapped['DataQualityService'] = relationship('DataQualityService', back_populates='data_quality_service_reports')


class DataQualityServicelinkmissingstopwarning(Base):
    __tablename__ = 'data_quality_servicelinkmissingstopwarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    service_link_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_servicelinkmissingstopwarning')
    data_quality_servicelinkmissingstopwarning_stops: Mapped[List['DataQualityServicelinkmissingstopwarningStops']] = relationship('DataQualityServicelinkmissingstopwarningStops', back_populates='servicelinkmissingstopwarning')


class DataQualitySlowlinkwarning(Base):
    __tablename__ = 'data_quality_slowlinkwarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_slowlinkwarning')
    timing_pattern: Mapped['DataQualityTimingpattern'] = relationship('DataQualityTimingpattern', back_populates='data_quality_slowlinkwarning')
    data_quality_slowlinkwarning_service_links: Mapped[List['DataQualitySlowlinkwarningServiceLinks']] = relationship('DataQualitySlowlinkwarningServiceLinks', back_populates='slowlinkwarning')
    data_quality_slowlinkwarning_timings: Mapped[List['DataQualitySlowlinkwarningTimings']] = relationship('DataQualitySlowlinkwarningTimings', back_populates='slowlinkwarning')


class DataQualitySlowtimingwarning(Base):
    __tablename__ = 'data_quality_slowtimingwarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_slowtimingwarning')
    timing_pattern: Mapped['DataQualityTimingpattern'] = relationship('DataQualityTimingpattern', back_populates='data_quality_slowtimingwarning')
    data_quality_slowtimingwarning_service_links: Mapped[List['DataQualitySlowtimingwarningServiceLinks']] = relationship('DataQualitySlowtimingwarningServiceLinks', back_populates='slowtimingwarning')
    data_quality_slowtimingwarning_timings: Mapped[List['DataQualitySlowtimingwarningTimings']] = relationship('DataQualitySlowtimingwarningTimings', back_populates='slowtimingwarning')


class DataQualityStopincorrecttypewarning(Base):
    __tablename__ = 'data_quality_stopincorrecttypewarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    stop_type: Mapped[str] = mapped_column(Text)
    report_id: Mapped[int] = mapped_column(Integer)
    stop_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_stopincorrecttypewarning')
    data_quality_stopincorrecttypewarning_service_patterns: Mapped[List['DataQualityStopincorrecttypewarningServicePatterns']] = relationship('DataQualityStopincorrecttypewarningServicePatterns', back_populates='stopincorrecttypewarning')


class DataQualityStopmissingnaptanwarning(Base):
    __tablename__ = 'data_quality_stopmissingnaptanwarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    stop_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_stopmissingnaptanwarning')
    data_quality_stopmissingnaptanwarning_service_patterns: Mapped[List['DataQualityStopmissingnaptanwarningServicePatterns']] = relationship('DataQualityStopmissingnaptanwarningServicePatterns', back_populates='stopmissingnaptanwarning')


class DataQualityTaskresults(Base):
    __tablename__ = 'data_quality_taskresults'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    status: Mapped[str] = mapped_column(String(64))
    message: Mapped[str] = mapped_column(Text)
    checks_id: Mapped[Optional[int]] = mapped_column(Integer)
    dataquality_report_id: Mapped[Optional[int]] = mapped_column(Integer)
    transmodel_txcfileattributes_id: Mapped[Optional[int]] = mapped_column(Integer)

    checks: Mapped[Optional['DataQualityChecks']] = relationship('DataQualityChecks', back_populates='data_quality_taskresults')
    dataquality_report: Mapped[Optional['DataQualityReport']] = relationship('DataQualityReport', back_populates='data_quality_taskresults')
    transmodel_txcfileattributes: Mapped[Optional['OrganisationTxcfileattributes']] = relationship('OrganisationTxcfileattributes', back_populates='data_quality_taskresults')
    data_quality_observationresults: Mapped[List['DataQualityObservationresults']] = relationship('DataQualityObservationresults', back_populates='taskresults')


class DataQualityTimingbackwardswarning(Base):
    __tablename__ = 'data_quality_timingbackwardswarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)
    from_stop_id: Mapped[int] = mapped_column(Integer)
    to_stop_id: Mapped[int] = mapped_column(Integer)

    from_stop: Mapped['DataQualityTimingpatternstop'] = relationship('DataQualityTimingpatternstop', back_populates='data_quality_timingbackwardswarning')
    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_timingbackwardswarning')
    timing_pattern: Mapped['DataQualityTimingpattern'] = relationship('DataQualityTimingpattern', back_populates='data_quality_timingbackwardswarning')
    to_stop: Mapped['DataQualityTimingpatternstop'] = relationship('DataQualityTimingpatternstop', back_populates='data_quality_timingbackwardswarning_')
    data_quality_timingbackwardswarning_service_links: Mapped[List['DataQualityTimingbackwardswarningServiceLinks']] = relationship('DataQualityTimingbackwardswarningServiceLinks', back_populates='timingbackwardswarning')
    data_quality_timingbackwardswarning_timings: Mapped[List['DataQualityTimingbackwardswarningTimings']] = relationship('DataQualityTimingbackwardswarningTimings', back_populates='timingbackwardswarning')


class DataQualityTimingdropoffwarning(Base):
    __tablename__ = 'data_quality_timingdropoffwarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_timingdropoffwarning')
    timing_pattern: Mapped['DataQualityTimingpattern'] = relationship('DataQualityTimingpattern', back_populates='data_quality_timingdropoffwarning')
    data_quality_timingdropoffwarning_service_links: Mapped[List['DataQualityTimingdropoffwarningServiceLinks']] = relationship('DataQualityTimingdropoffwarningServiceLinks', back_populates='timingdropoffwarning')
    data_quality_timingdropoffwarning_timings: Mapped[List['DataQualityTimingdropoffwarningTimings']] = relationship('DataQualityTimingdropoffwarningTimings', back_populates='timingdropoffwarning')


class DataQualityTimingfirstwarning(Base):
    __tablename__ = 'data_quality_timingfirstwarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_timingfirstwarning')
    timing_pattern: Mapped['DataQualityTimingpattern'] = relationship('DataQualityTimingpattern', back_populates='data_quality_timingfirstwarning')
    data_quality_timingfirstwarning_service_links: Mapped[List['DataQualityTimingfirstwarningServiceLinks']] = relationship('DataQualityTimingfirstwarningServiceLinks', back_populates='timingfirstwarning')
    data_quality_timingfirstwarning_timings: Mapped[List['DataQualityTimingfirstwarningTimings']] = relationship('DataQualityTimingfirstwarningTimings', back_populates='timingfirstwarning')


class DataQualityTiminglastwarning(Base):
    __tablename__ = 'data_quality_timinglastwarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_timinglastwarning')
    timing_pattern: Mapped['DataQualityTimingpattern'] = relationship('DataQualityTimingpattern', back_populates='data_quality_timinglastwarning')
    data_quality_timinglastwarning_service_links: Mapped[List['DataQualityTiminglastwarningServiceLinks']] = relationship('DataQualityTiminglastwarningServiceLinks', back_populates='timinglastwarning')
    data_quality_timinglastwarning_timings: Mapped[List['DataQualityTiminglastwarningTimings']] = relationship('DataQualityTiminglastwarningTimings', back_populates='timinglastwarning')


class DataQualityTimingmissingpointwarning(Base):
    __tablename__ = 'data_quality_timingmissingpointwarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_timingmissingpointwarning')
    timing_pattern: Mapped['DataQualityTimingpattern'] = relationship('DataQualityTimingpattern', back_populates='data_quality_timingmissingpointwarning')
    data_quality_timingmissingpointwarning_service_links: Mapped[List['DataQualityTimingmissingpointwarningServiceLinks']] = relationship('DataQualityTimingmissingpointwarningServiceLinks', back_populates='timingmissingpointwarning')
    data_quality_timingmissingpointwarning_timings: Mapped[List['DataQualityTimingmissingpointwarningTimings']] = relationship('DataQualityTimingmissingpointwarningTimings', back_populates='timingmissingpointwarning')


class DataQualityTimingmultiplewarning(Base):
    __tablename__ = 'data_quality_timingmultiplewarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_timingmultiplewarning')
    timing_pattern: Mapped['DataQualityTimingpattern'] = relationship('DataQualityTimingpattern', back_populates='data_quality_timingmultiplewarning')
    data_quality_timingmultiplewarning_timings: Mapped[List['DataQualityTimingmultiplewarningTimings']] = relationship('DataQualityTimingmultiplewarningTimings', back_populates='timingmultiplewarning')


class DataQualityTimingpickupwarning(Base):
    __tablename__ = 'data_quality_timingpickupwarning'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped['DataQualityDataqualityreport'] = relationship('DataQualityDataqualityreport', back_populates='data_quality_timingpickupwarning')
    timing_pattern: Mapped['DataQualityTimingpattern'] = relationship('DataQualityTimingpattern', back_populates='data_quality_timingpickupwarning')
    data_quality_timingpickupwarning_service_links: Mapped[List['DataQualityTimingpickupwarningServiceLinks']] = relationship('DataQualityTimingpickupwarningServiceLinks', back_populates='timingpickupwarning')
    data_quality_timingpickupwarning_timings: Mapped[List['DataQualityTimingpickupwarningTimings']] = relationship('DataQualityTimingpickupwarningTimings', back_populates='timingpickupwarning')


class DqsTaskresults(Base):
    __tablename__ = 'dqs_taskresults'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    status: Mapped[str] = mapped_column(String(64))
    message: Mapped[str] = mapped_column(Text)
    checks_id: Mapped[Optional[int]] = mapped_column(Integer)
    dataquality_report_id: Mapped[Optional[int]] = mapped_column(Integer)
    transmodel_txcfileattributes_id: Mapped[Optional[int]] = mapped_column(Integer)

    checks: Mapped[Optional['DqsChecks']] = relationship('DqsChecks', back_populates='dqs_taskresults')
    dataquality_report: Mapped[Optional['DqsReport']] = relationship('DqsReport', back_populates='dqs_taskresults')
    transmodel_txcfileattributes: Mapped[Optional['OrganisationTxcfileattributes']] = relationship('OrganisationTxcfileattributes', back_populates='dqs_taskresults')
    dqs_observationresults: Mapped[List['DqsObservationresults']] = relationship('DqsObservationresults', back_populates='taskresults')


class FaresFaresmetadata(OrganisationDatasetmetadata):
    __tablename__ = 'fares_faresmetadata'

    datasetmetadata_ptr_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    num_of_fare_zones: Mapped[int] = mapped_column(Integer)
    num_of_lines: Mapped[int] = mapped_column(Integer)
    num_of_sales_offer_packages: Mapped[int] = mapped_column(Integer)
    num_of_fare_products: Mapped[int] = mapped_column(Integer)
    num_of_user_profiles: Mapped[int] = mapped_column(Integer)
    valid_from: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    valid_to: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    num_of_pass_products: Mapped[Optional[int]] = mapped_column(Integer)
    num_of_trip_products: Mapped[Optional[int]] = mapped_column(Integer)

    fares_datacataloguemetadata: Mapped[List['FaresDatacataloguemetadata']] = relationship('FaresDatacataloguemetadata', back_populates='fares_metadata')
    fares_faresmetadata_stops: Mapped[List['FaresFaresmetadataStops']] = relationship('FaresFaresmetadataStops', back_populates='faresmetadata')


class FaresValidatorFaresvalidation(Base):
    __tablename__ = 'fares_validator_faresvalidation'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    file_name: Mapped[str] = mapped_column(String(256))
    error_line_no: Mapped[int] = mapped_column(Integer)
    type_of_observation: Mapped[str] = mapped_column(String(1024))
    category: Mapped[str] = mapped_column(String(1024))
    error: Mapped[str] = mapped_column(String(2000))
    reference: Mapped[str] = mapped_column(String(1024))
    important_note: Mapped[str] = mapped_column(String(2000))
    organisation_id: Mapped[int] = mapped_column(Integer)
    revision_id: Mapped[int] = mapped_column(Integer)

    organisation: Mapped['OrganisationOrganisation'] = relationship('OrganisationOrganisation', back_populates='fares_validator_faresvalidation')
    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='fares_validator_faresvalidation')


class FaresValidatorFaresvalidationresult(Base):
    __tablename__ = 'fares_validator_faresvalidationresult'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    count: Mapped[int] = mapped_column(Integer)
    report_file_name: Mapped[str] = mapped_column(String(256))
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    organisation_id: Mapped[int] = mapped_column(Integer)
    revision_id: Mapped[int] = mapped_column(Integer)

    organisation: Mapped['OrganisationOrganisation'] = relationship('OrganisationOrganisation', back_populates='fares_validator_faresvalidationresult')
    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='fares_validator_faresvalidationresult')


class NaptanLocality(Base):
    __tablename__ = 'naptan_locality'

    gazetteer_id: Mapped[str] = mapped_column(String(8), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    easting: Mapped[int] = mapped_column(Integer)
    northing: Mapped[int] = mapped_column(Integer)
    admin_area_id: Mapped[Optional[int]] = mapped_column(Integer)
    district_id: Mapped[Optional[int]] = mapped_column(Integer)

    admin_area: Mapped[Optional['NaptanAdminarea']] = relationship('NaptanAdminarea', back_populates='naptan_locality')
    district: Mapped[Optional['NaptanDistrict']] = relationship('NaptanDistrict', back_populates='naptan_locality')
    naptan_stoppoint: Mapped[List['NaptanStoppoint']] = relationship('NaptanStoppoint', back_populates='locality')
    organisation_datasetrevision_localities: Mapped[List['OrganisationDatasetrevisionLocalities']] = relationship('OrganisationDatasetrevisionLocalities', back_populates='locality')
    transmodel_servicepattern_localities: Mapped[List['TransmodelServicepatternLocalities']] = relationship('TransmodelServicepatternLocalities', back_populates='locality')


class OrganisationConsumerstats(Base):
    __tablename__ = 'organisation_consumerstats'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    monthly_breakdown: Mapped[str] = mapped_column(String(100))
    weekly_unique_consumers: Mapped[int] = mapped_column(Integer)
    weekly_downloads: Mapped[int] = mapped_column(Integer)
    weekly_api_hits: Mapped[int] = mapped_column(Integer)
    organisation_id: Mapped[int] = mapped_column(Integer)

    organisation: Mapped['OrganisationOrganisation'] = relationship('OrganisationOrganisation', back_populates='organisation_consumerstats')


class OrganisationDatasetrevisionAdminAreas(Base):
    __tablename__ = 'organisation_datasetrevision_admin_areas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    datasetrevision_id: Mapped[int] = mapped_column(Integer)
    adminarea_id: Mapped[int] = mapped_column(Integer)

    adminarea: Mapped['NaptanAdminarea'] = relationship('NaptanAdminarea', back_populates='organisation_datasetrevision_admin_areas')
    datasetrevision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='organisation_datasetrevision_admin_areas')


class OrganisationLicence(Base):
    __tablename__ = 'organisation_licence'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(9))
    organisation_id: Mapped[int] = mapped_column(Integer)

    organisation: Mapped['OrganisationOrganisation'] = relationship('OrganisationOrganisation', back_populates='organisation_licence')
    organisation_seasonalservice: Mapped[List['OrganisationSeasonalservice']] = relationship('OrganisationSeasonalservice', back_populates='licence')
    organisation_servicecodeexemption: Mapped[List['OrganisationServicecodeexemption']] = relationship('OrganisationServicecodeexemption', back_populates='licence')


class OrganisationOperatorcode(Base):
    __tablename__ = 'organisation_operatorcode'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    noc: Mapped[str] = mapped_column(String(20))
    organisation_id: Mapped[int] = mapped_column(Integer)

    organisation: Mapped['OrganisationOrganisation'] = relationship('OrganisationOrganisation', back_populates='organisation_operatorcode')


class OrganisationOrganisationAdminAreas(Base):
    __tablename__ = 'organisation_organisation_admin_areas'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    organisation_id: Mapped[int] = mapped_column(Integer)
    adminarea_id: Mapped[int] = mapped_column(Integer)

    adminarea: Mapped['NaptanAdminarea'] = relationship('NaptanAdminarea', back_populates='organisation_organisation_admin_areas')
    organisation: Mapped['OrganisationOrganisation'] = relationship('OrganisationOrganisation', back_populates='organisation_organisation_admin_areas')


class OtcLocalauthorityRegistrationNumbers(Base):
    __tablename__ = 'otc_localauthority_registration_numbers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    localauthority_id: Mapped[int] = mapped_column(Integer)
    service_id: Mapped[int] = mapped_column(Integer)

    localauthority: Mapped['OtcLocalauthority'] = relationship('OtcLocalauthority', back_populates='otc_localauthority_registration_numbers')
    service: Mapped['OtcService'] = relationship('OtcService', back_populates='otc_localauthority_registration_numbers')


class PipelinesDataqualitytask(Base):
    __tablename__ = 'pipelines_dataqualitytask'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    status: Mapped[str] = mapped_column(String(50))
    revision_id: Mapped[int] = mapped_column(Integer)
    message: Mapped[str] = mapped_column(Text)
    task_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    report_id: Mapped[Optional[int]] = mapped_column(Integer)
    completed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    report: Mapped[Optional['DataQualityDataqualityreport']] = relationship('DataQualityDataqualityreport', back_populates='pipelines_dataqualitytask')
    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='pipelines_dataqualitytask')


class TransmodelService(Base):
    __tablename__ = 'transmodel_service'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_code: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    other_names: Mapped[list] = mapped_column(ARRAY(String(length=255)))
    start_date: Mapped[datetime.date] = mapped_column(Date)
    service_type: Mapped[str] = mapped_column(String(255))
    end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    revision_id: Mapped[Optional[int]] = mapped_column(Integer)
    txcfileattributes_id: Mapped[Optional[int]] = mapped_column(Integer)

    revision: Mapped[Optional['OrganisationDatasetrevision']] = relationship('OrganisationDatasetrevision', back_populates='transmodel_service')
    txcfileattributes: Mapped[Optional['OrganisationTxcfileattributes']] = relationship('OrganisationTxcfileattributes', back_populates='transmodel_service')
    transmodel_bookingarrangements: Mapped[List['TransmodelBookingarrangements']] = relationship('TransmodelBookingarrangements', back_populates='service')
    transmodel_service_service_patterns: Mapped[List['TransmodelServiceServicePatterns']] = relationship('TransmodelServiceServicePatterns', back_populates='service')
    organisation_consumerfeedback: Mapped[List['OrganisationConsumerfeedback']] = relationship('OrganisationConsumerfeedback', back_populates='service')


class TransmodelServicepatternAdminAreas(Base):
    __tablename__ = 'transmodel_servicepattern_admin_areas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    servicepattern_id: Mapped[int] = mapped_column(Integer)
    adminarea_id: Mapped[int] = mapped_column(Integer)

    adminarea: Mapped['NaptanAdminarea'] = relationship('NaptanAdminarea', back_populates='transmodel_servicepattern_admin_areas')


class TransmodelVehiclejourney(Base):
    __tablename__ = 'transmodel_vehiclejourney'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    departure_day_shift: Mapped[bool] = mapped_column(Boolean)
    start_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    direction: Mapped[Optional[str]] = mapped_column(String(255))
    journey_code: Mapped[Optional[str]] = mapped_column(String(255))
    line_ref: Mapped[Optional[str]] = mapped_column(String(255))
    service_pattern_id: Mapped[Optional[int]] = mapped_column(Integer)
    block_number: Mapped[Optional[str]] = mapped_column(String(20))

    service_pattern: Mapped[Optional['TransmodelServicepattern']] = relationship('TransmodelServicepattern', back_populates='transmodel_vehiclejourney')
    transmodel_flexibleserviceoperationperiod: Mapped[List['TransmodelFlexibleserviceoperationperiod']] = relationship('TransmodelFlexibleserviceoperationperiod', back_populates='vehicle_journey')
    transmodel_nonoperatingdatesexceptions: Mapped[List['TransmodelNonoperatingdatesexceptions']] = relationship('TransmodelNonoperatingdatesexceptions', back_populates='vehicle_journey')
    transmodel_operatingdatesexceptions: Mapped[List['TransmodelOperatingdatesexceptions']] = relationship('TransmodelOperatingdatesexceptions', back_populates='vehicle_journey')
    transmodel_operatingprofile: Mapped[List['TransmodelOperatingprofile']] = relationship('TransmodelOperatingprofile', back_populates='vehicle_journey')
    transmodel_servicedorganisationvehiclejourney: Mapped[List['TransmodelServicedorganisationvehiclejourney']] = relationship('TransmodelServicedorganisationvehiclejourney', back_populates='vehicle_journey')
    transmodel_servicepatternstop: Mapped[List['TransmodelServicepatternstop']] = relationship('TransmodelServicepatternstop', back_populates='vehicle_journey')
    transmodel_tracksvehiclejourney: Mapped[List['TransmodelTracksvehiclejourney']] = relationship('TransmodelTracksvehiclejourney', back_populates='vehicle_journey')
    data_quality_observationresults: Mapped[List['DataQualityObservationresults']] = relationship('DataQualityObservationresults', back_populates='vehicle_journey')
    dqs_observationresults: Mapped[List['DqsObservationresults']] = relationship('DqsObservationresults', back_populates='vehicle_journey')
    organisation_consumerfeedback: Mapped[List['OrganisationConsumerfeedback']] = relationship('OrganisationConsumerfeedback', back_populates='vehicle_journey')


class UsersInvitation(InvitationsInvitation):
    __tablename__ = 'users_invitation'

    invitation_ptr_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    account_type: Mapped[int] = mapped_column(Integer)
    is_key_contact: Mapped[bool] = mapped_column(Boolean)
    organisation_id: Mapped[Optional[int]] = mapped_column(Integer)

    organisation: Mapped[Optional['OrganisationOrganisation']] = relationship('OrganisationOrganisation', back_populates='users_invitation')
    users_agentuserinvite: Mapped[List['UsersAgentuserinvite']] = relationship('UsersAgentuserinvite', back_populates='invitation')


class UsersUserOrganisations(Base):
    __tablename__ = 'users_user_organisations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    organisation_id: Mapped[int] = mapped_column(Integer)

    organisation: Mapped['OrganisationOrganisation'] = relationship('OrganisationOrganisation', back_populates='users_user_organisations')
    user: Mapped['UsersUser'] = relationship('UsersUser', back_populates='users_user_organisations')


class UsersUserUserPermissions(Base):
    __tablename__ = 'users_user_user_permissions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    permission_id: Mapped[int] = mapped_column(Integer)

    permission: Mapped['AuthPermission'] = relationship('AuthPermission', back_populates='users_user_user_permissions')
    user: Mapped['UsersUser'] = relationship('UsersUser', back_populates='users_user_user_permissions')


class DataQualityFastlinkwarningServiceLinks(Base):
    __tablename__ = 'data_quality_fastlinkwarning_service_links'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fastlinkwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    fastlinkwarning: Mapped['DataQualityFastlinkwarning'] = relationship('DataQualityFastlinkwarning', back_populates='data_quality_fastlinkwarning_service_links')


class DataQualityFastlinkwarningTimings(Base):
    __tablename__ = 'data_quality_fastlinkwarning_timings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fastlinkwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    fastlinkwarning: Mapped['DataQualityFastlinkwarning'] = relationship('DataQualityFastlinkwarning', back_populates='data_quality_fastlinkwarning_timings')
    timingpatternstop: Mapped['DataQualityTimingpatternstop'] = relationship('DataQualityTimingpatternstop', back_populates='data_quality_fastlinkwarning_timings')


class DataQualityFasttimingwarningServiceLinks(Base):
    __tablename__ = 'data_quality_fasttimingwarning_service_links'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fasttimingwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    fasttimingwarning: Mapped['DataQualityFasttimingwarning'] = relationship('DataQualityFasttimingwarning', back_populates='data_quality_fasttimingwarning_service_links')


class DataQualityFasttimingwarningTimings(Base):
    __tablename__ = 'data_quality_fasttimingwarning_timings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fasttimingwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    fasttimingwarning: Mapped['DataQualityFasttimingwarning'] = relationship('DataQualityFasttimingwarning', back_populates='data_quality_fasttimingwarning_timings')
    timingpatternstop: Mapped['DataQualityTimingpatternstop'] = relationship('DataQualityTimingpatternstop', back_populates='data_quality_fasttimingwarning_timings')


class DataQualityJourneyconflictwarningStops(Base):
    __tablename__ = 'data_quality_journeyconflictwarning_stops'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    journeyconflictwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    stoppoint_id: Mapped[int] = mapped_column(Integer)

    journeyconflictwarning: Mapped['DataQualityJourneyconflictwarning'] = relationship('DataQualityJourneyconflictwarning', back_populates='data_quality_journeyconflictwarning_stops')


class DataQualityJourneystopinappropriatewarningVehicleJourneys(Base):
    __tablename__ = 'data_quality_journeystopinappropriatewarning_vehicle_journeys'

    id: Mapped[int] = mapped_column(Integer, Sequence('data_quality_journeystopinappropriatewarning_vehicle_jou_id_seq'), primary_key=True)
    journeystopinappropriatewarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    vehiclejourney_id: Mapped[int] = mapped_column(Integer)

    journeystopinappropriatewarning: Mapped['DataQualityJourneystopinappropriatewarning'] = relationship('DataQualityJourneystopinappropriatewarning', back_populates='data_quality_journeystopinappropriatewarning_vehicle_journeys')
    vehiclejourney: Mapped['DataQualityVehiclejourney'] = relationship('DataQualityVehiclejourney', back_populates='data_quality_journeystopinappropriatewarning_vehicle_journeys')


class DataQualityLineexpiredwarningVehicleJourneys(Base):
    __tablename__ = 'data_quality_lineexpiredwarning_vehicle_journeys'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lineexpiredwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    vehiclejourney_id: Mapped[int] = mapped_column(Integer)

    lineexpiredwarning: Mapped['DataQualityLineexpiredwarning'] = relationship('DataQualityLineexpiredwarning', back_populates='data_quality_lineexpiredwarning_vehicle_journeys')
    vehiclejourney: Mapped['DataQualityVehiclejourney'] = relationship('DataQualityVehiclejourney', back_populates='data_quality_lineexpiredwarning_vehicle_journeys')


class DataQualityLinemissingblockidwarningVehicleJourneys(Base):
    __tablename__ = 'data_quality_linemissingblockidwarning_vehicle_journeys'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    linemissingblockidwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    vehiclejourney_id: Mapped[int] = mapped_column(Integer)

    linemissingblockidwarning: Mapped['DataQualityLinemissingblockidwarning'] = relationship('DataQualityLinemissingblockidwarning', back_populates='data_quality_linemissingblockidwarning_vehicle_journeys')
    vehiclejourney: Mapped['DataQualityVehiclejourney'] = relationship('DataQualityVehiclejourney', back_populates='data_quality_linemissingblockidwarning_vehicle_journeys')


class DataQualityServicelinkmissingstopwarningStops(Base):
    __tablename__ = 'data_quality_servicelinkmissingstopwarning_stops'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    servicelinkmissingstopwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    stoppoint_id: Mapped[int] = mapped_column(Integer)

    servicelinkmissingstopwarning: Mapped['DataQualityServicelinkmissingstopwarning'] = relationship('DataQualityServicelinkmissingstopwarning', back_populates='data_quality_servicelinkmissingstopwarning_stops')


class DataQualitySlowlinkwarningServiceLinks(Base):
    __tablename__ = 'data_quality_slowlinkwarning_service_links'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slowlinkwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    slowlinkwarning: Mapped['DataQualitySlowlinkwarning'] = relationship('DataQualitySlowlinkwarning', back_populates='data_quality_slowlinkwarning_service_links')


class DataQualitySlowlinkwarningTimings(Base):
    __tablename__ = 'data_quality_slowlinkwarning_timings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slowlinkwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    slowlinkwarning: Mapped['DataQualitySlowlinkwarning'] = relationship('DataQualitySlowlinkwarning', back_populates='data_quality_slowlinkwarning_timings')
    timingpatternstop: Mapped['DataQualityTimingpatternstop'] = relationship('DataQualityTimingpatternstop', back_populates='data_quality_slowlinkwarning_timings')


class DataQualitySlowtimingwarningServiceLinks(Base):
    __tablename__ = 'data_quality_slowtimingwarning_service_links'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slowtimingwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    slowtimingwarning: Mapped['DataQualitySlowtimingwarning'] = relationship('DataQualitySlowtimingwarning', back_populates='data_quality_slowtimingwarning_service_links')


class DataQualitySlowtimingwarningTimings(Base):
    __tablename__ = 'data_quality_slowtimingwarning_timings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slowtimingwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    slowtimingwarning: Mapped['DataQualitySlowtimingwarning'] = relationship('DataQualitySlowtimingwarning', back_populates='data_quality_slowtimingwarning_timings')
    timingpatternstop: Mapped['DataQualityTimingpatternstop'] = relationship('DataQualityTimingpatternstop', back_populates='data_quality_slowtimingwarning_timings')


class DataQualityStopincorrecttypewarningServicePatterns(Base):
    __tablename__ = 'data_quality_stopincorrecttypewarning_service_patterns'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stopincorrecttypewarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicepattern_id: Mapped[int] = mapped_column(Integer)

    stopincorrecttypewarning: Mapped['DataQualityStopincorrecttypewarning'] = relationship('DataQualityStopincorrecttypewarning', back_populates='data_quality_stopincorrecttypewarning_service_patterns')


class DataQualityStopmissingnaptanwarningServicePatterns(Base):
    __tablename__ = 'data_quality_stopmissingnaptanwarning_service_patterns'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stopmissingnaptanwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicepattern_id: Mapped[int] = mapped_column(Integer)

    stopmissingnaptanwarning: Mapped['DataQualityStopmissingnaptanwarning'] = relationship('DataQualityStopmissingnaptanwarning', back_populates='data_quality_stopmissingnaptanwarning_service_patterns')


class DataQualityTimingbackwardswarningServiceLinks(Base):
    __tablename__ = 'data_quality_timingbackwardswarning_service_links'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingbackwardswarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    timingbackwardswarning: Mapped['DataQualityTimingbackwardswarning'] = relationship('DataQualityTimingbackwardswarning', back_populates='data_quality_timingbackwardswarning_service_links')


class DataQualityTimingbackwardswarningTimings(Base):
    __tablename__ = 'data_quality_timingbackwardswarning_timings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingbackwardswarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    timingbackwardswarning: Mapped['DataQualityTimingbackwardswarning'] = relationship('DataQualityTimingbackwardswarning', back_populates='data_quality_timingbackwardswarning_timings')
    timingpatternstop: Mapped['DataQualityTimingpatternstop'] = relationship('DataQualityTimingpatternstop', back_populates='data_quality_timingbackwardswarning_timings')


class DataQualityTimingdropoffwarningServiceLinks(Base):
    __tablename__ = 'data_quality_timingdropoffwarning_service_links'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingdropoffwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    timingdropoffwarning: Mapped['DataQualityTimingdropoffwarning'] = relationship('DataQualityTimingdropoffwarning', back_populates='data_quality_timingdropoffwarning_service_links')


class DataQualityTimingdropoffwarningTimings(Base):
    __tablename__ = 'data_quality_timingdropoffwarning_timings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingdropoffwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    timingdropoffwarning: Mapped['DataQualityTimingdropoffwarning'] = relationship('DataQualityTimingdropoffwarning', back_populates='data_quality_timingdropoffwarning_timings')
    timingpatternstop: Mapped['DataQualityTimingpatternstop'] = relationship('DataQualityTimingpatternstop', back_populates='data_quality_timingdropoffwarning_timings')


class DataQualityTimingfirstwarningServiceLinks(Base):
    __tablename__ = 'data_quality_timingfirstwarning_service_links'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingfirstwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    timingfirstwarning: Mapped['DataQualityTimingfirstwarning'] = relationship('DataQualityTimingfirstwarning', back_populates='data_quality_timingfirstwarning_service_links')


class DataQualityTimingfirstwarningTimings(Base):
    __tablename__ = 'data_quality_timingfirstwarning_timings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingfirstwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    timingfirstwarning: Mapped['DataQualityTimingfirstwarning'] = relationship('DataQualityTimingfirstwarning', back_populates='data_quality_timingfirstwarning_timings')
    timingpatternstop: Mapped['DataQualityTimingpatternstop'] = relationship('DataQualityTimingpatternstop', back_populates='data_quality_timingfirstwarning_timings')


class DataQualityTiminglastwarningServiceLinks(Base):
    __tablename__ = 'data_quality_timinglastwarning_service_links'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timinglastwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    timinglastwarning: Mapped['DataQualityTiminglastwarning'] = relationship('DataQualityTiminglastwarning', back_populates='data_quality_timinglastwarning_service_links')


class DataQualityTiminglastwarningTimings(Base):
    __tablename__ = 'data_quality_timinglastwarning_timings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timinglastwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    timinglastwarning: Mapped['DataQualityTiminglastwarning'] = relationship('DataQualityTiminglastwarning', back_populates='data_quality_timinglastwarning_timings')
    timingpatternstop: Mapped['DataQualityTimingpatternstop'] = relationship('DataQualityTimingpatternstop', back_populates='data_quality_timinglastwarning_timings')


class DataQualityTimingmissingpointwarningServiceLinks(Base):
    __tablename__ = 'data_quality_timingmissingpointwarning_service_links'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingmissingpointwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    timingmissingpointwarning: Mapped['DataQualityTimingmissingpointwarning'] = relationship('DataQualityTimingmissingpointwarning', back_populates='data_quality_timingmissingpointwarning_service_links')


class DataQualityTimingmissingpointwarningTimings(Base):
    __tablename__ = 'data_quality_timingmissingpointwarning_timings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingmissingpointwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    timingmissingpointwarning: Mapped['DataQualityTimingmissingpointwarning'] = relationship('DataQualityTimingmissingpointwarning', back_populates='data_quality_timingmissingpointwarning_timings')
    timingpatternstop: Mapped['DataQualityTimingpatternstop'] = relationship('DataQualityTimingpatternstop', back_populates='data_quality_timingmissingpointwarning_timings')


class DataQualityTimingmultiplewarningTimings(Base):
    __tablename__ = 'data_quality_timingmultiplewarning_timings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingmultiplewarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    timingmultiplewarning: Mapped['DataQualityTimingmultiplewarning'] = relationship('DataQualityTimingmultiplewarning', back_populates='data_quality_timingmultiplewarning_timings')
    timingpatternstop: Mapped['DataQualityTimingpatternstop'] = relationship('DataQualityTimingpatternstop', back_populates='data_quality_timingmultiplewarning_timings')


class DataQualityTimingpickupwarningServiceLinks(Base):
    __tablename__ = 'data_quality_timingpickupwarning_service_links'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingpickupwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    timingpickupwarning: Mapped['DataQualityTimingpickupwarning'] = relationship('DataQualityTimingpickupwarning', back_populates='data_quality_timingpickupwarning_service_links')


class DataQualityTimingpickupwarningTimings(Base):
    __tablename__ = 'data_quality_timingpickupwarning_timings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingpickupwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    timingpatternstop: Mapped['DataQualityTimingpatternstop'] = relationship('DataQualityTimingpatternstop', back_populates='data_quality_timingpickupwarning_timings')
    timingpickupwarning: Mapped['DataQualityTimingpickupwarning'] = relationship('DataQualityTimingpickupwarning', back_populates='data_quality_timingpickupwarning_timings')


class FaresDatacataloguemetadata(Base):
    __tablename__ = 'fares_datacataloguemetadata'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    xml_file_name: Mapped[str] = mapped_column(String(255))
    fares_metadata_id: Mapped[int] = mapped_column(Integer)
    valid_from: Mapped[Optional[datetime.date]] = mapped_column(Date)
    valid_to: Mapped[Optional[datetime.date]] = mapped_column(Date)
    national_operator_code: Mapped[Optional[list]] = mapped_column(ARRAY(String(length=255)))
    line_id: Mapped[Optional[list]] = mapped_column(ARRAY(String(length=100)))
    line_name: Mapped[Optional[list]] = mapped_column(ARRAY(String(length=100)))
    atco_area: Mapped[Optional[list]] = mapped_column(ARRAY(Integer()))
    tariff_basis: Mapped[Optional[list]] = mapped_column(ARRAY(String(length=100)))
    product_type: Mapped[Optional[list]] = mapped_column(ARRAY(String(length=100)))
    product_name: Mapped[Optional[list]] = mapped_column(ARRAY(String(length=100)))
    user_type: Mapped[Optional[list]] = mapped_column(ARRAY(String(length=100)))

    fares_metadata: Mapped['FaresFaresmetadata'] = relationship('FaresFaresmetadata', back_populates='fares_datacataloguemetadata')


class FaresFaresmetadataStops(Base):
    __tablename__ = 'fares_faresmetadata_stops'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    faresmetadata_id: Mapped[int] = mapped_column(Integer)
    stoppoint_id: Mapped[int] = mapped_column(Integer)

    faresmetadata: Mapped['FaresFaresmetadata'] = relationship('FaresFaresmetadata', back_populates='fares_faresmetadata_stops')


class NaptanStoppoint(Base):
    __tablename__ = 'naptan_stoppoint'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    atco_code: Mapped[str] = mapped_column(String(255))
    common_name: Mapped[str] = mapped_column(String(255))
    location: Mapped[Any] = mapped_column(Geometry('POINT', 4326, from_text='ST_GeomFromEWKT', name='geometry', nullable=False))
    stop_areas: Mapped[list] = mapped_column(ARRAY(String(length=255)))
    naptan_code: Mapped[Optional[str]] = mapped_column(String(12))
    street: Mapped[Optional[str]] = mapped_column(String(255))
    indicator: Mapped[Optional[str]] = mapped_column(String(255))
    admin_area_id: Mapped[Optional[int]] = mapped_column(Integer)
    locality_id: Mapped[Optional[str]] = mapped_column(String(8))
    bus_stop_type: Mapped[Optional[str]] = mapped_column(String(255))
    stop_type: Mapped[Optional[str]] = mapped_column(String(255))

    admin_area: Mapped[Optional['NaptanAdminarea']] = relationship('NaptanAdminarea', back_populates='naptan_stoppoint')
    locality: Mapped[Optional['NaptanLocality']] = relationship('NaptanLocality', back_populates='naptan_stoppoint')
    naptan_flexiblezone: Mapped[List['NaptanFlexiblezone']] = relationship('NaptanFlexiblezone', back_populates='naptan_stoppoint')


class OrganisationDatasetrevisionLocalities(Base):
    __tablename__ = 'organisation_datasetrevision_localities'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    datasetrevision_id: Mapped[int] = mapped_column(Integer)
    locality_id: Mapped[str] = mapped_column(String(8))

    datasetrevision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='organisation_datasetrevision_localities')
    locality: Mapped['NaptanLocality'] = relationship('NaptanLocality', back_populates='organisation_datasetrevision_localities')


class OrganisationSeasonalservice(Base):
    __tablename__ = 'organisation_seasonalservice'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    registration_code: Mapped[int] = mapped_column(Integer)
    start: Mapped[datetime.date] = mapped_column(Date)
    end: Mapped[datetime.date] = mapped_column(Date)
    licence_id: Mapped[int] = mapped_column(Integer)

    licence: Mapped['OrganisationLicence'] = relationship('OrganisationLicence', back_populates='organisation_seasonalservice')


class OrganisationServicecodeexemption(Base):
    __tablename__ = 'organisation_servicecodeexemption'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    registration_code: Mapped[str] = mapped_column(String(50))
    justification: Mapped[str] = mapped_column(String(140))
    exempted_by_id: Mapped[int] = mapped_column(Integer)
    licence_id: Mapped[int] = mapped_column(Integer)

    exempted_by: Mapped['UsersUser'] = relationship('UsersUser', back_populates='organisation_servicecodeexemption')
    licence: Mapped['OrganisationLicence'] = relationship('OrganisationLicence', back_populates='organisation_servicecodeexemption')


class TransmodelBookingarrangements(Base):
    __tablename__ = 'transmodel_bookingarrangements'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    service_id: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[Optional[str]] = mapped_column(String(254))
    phone_number: Mapped[Optional[str]] = mapped_column(String(16))
    web_address: Mapped[Optional[str]] = mapped_column(String(200))

    service: Mapped['TransmodelService'] = relationship('TransmodelService', back_populates='transmodel_bookingarrangements')


class TransmodelFlexibleserviceoperationperiod(Base):
    __tablename__ = 'transmodel_flexibleserviceoperationperiod'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)
    end_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    start_time: Mapped[Optional[datetime.time]] = mapped_column(Time)

    vehicle_journey: Mapped['TransmodelVehiclejourney'] = relationship('TransmodelVehiclejourney', back_populates='transmodel_flexibleserviceoperationperiod')


class TransmodelNonoperatingdatesexceptions(Base):
    __tablename__ = 'transmodel_nonoperatingdatesexceptions'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)
    non_operating_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    vehicle_journey: Mapped['TransmodelVehiclejourney'] = relationship('TransmodelVehiclejourney', back_populates='transmodel_nonoperatingdatesexceptions')


class TransmodelOperatingdatesexceptions(Base):
    __tablename__ = 'transmodel_operatingdatesexceptions'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)
    operating_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    vehicle_journey: Mapped['TransmodelVehiclejourney'] = relationship('TransmodelVehiclejourney', back_populates='transmodel_operatingdatesexceptions')


class TransmodelOperatingprofile(Base):
    __tablename__ = 'transmodel_operatingprofile'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    day_of_week: Mapped[str] = mapped_column(String(20))
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)

    vehicle_journey: Mapped['TransmodelVehiclejourney'] = relationship('TransmodelVehiclejourney', back_populates='transmodel_operatingprofile')


class TransmodelServiceServicePatterns(Base):
    __tablename__ = 'transmodel_service_service_patterns'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_id: Mapped[int] = mapped_column(Integer)
    servicepattern_id: Mapped[int] = mapped_column(Integer)

    service: Mapped['TransmodelService'] = relationship('TransmodelService', back_populates='transmodel_service_service_patterns')


class TransmodelServicedorganisationvehiclejourney(Base):
    __tablename__ = 'transmodel_servicedorganisationvehiclejourney'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    operating_on_working_days: Mapped[bool] = mapped_column(Boolean)
    serviced_organisation_id: Mapped[int] = mapped_column(Integer)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)

    serviced_organisation: Mapped['TransmodelServicedorganisations'] = relationship('TransmodelServicedorganisations', back_populates='transmodel_servicedorganisationvehiclejourney')
    vehicle_journey: Mapped['TransmodelVehiclejourney'] = relationship('TransmodelVehiclejourney', back_populates='transmodel_servicedorganisationvehiclejourney')
    dqs_observationresults: Mapped[List['DqsObservationresults']] = relationship('DqsObservationresults', back_populates='serviced_organisation_vehicle_journey')
    transmodel_servicedorganisationworkingdays: Mapped[List['TransmodelServicedorganisationworkingdays']] = relationship('TransmodelServicedorganisationworkingdays', back_populates='serviced_organisation_vehicle_journey')


class TransmodelServicepatternLocalities(Base):
    __tablename__ = 'transmodel_servicepattern_localities'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    servicepattern_id: Mapped[int] = mapped_column(Integer)
    locality_id: Mapped[str] = mapped_column(String(8))

    locality: Mapped['NaptanLocality'] = relationship('NaptanLocality', back_populates='transmodel_servicepattern_localities')


class TransmodelServicepatternstop(Base):
    __tablename__ = 'transmodel_servicepatternstop'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sequence_number: Mapped[int] = mapped_column(Integer)
    atco_code: Mapped[str] = mapped_column(String(255))
    service_pattern_id: Mapped[int] = mapped_column(Integer)
    is_timing_point: Mapped[bool] = mapped_column(Boolean)
    naptan_stop_id: Mapped[Optional[int]] = mapped_column(Integer)
    departure_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    txc_common_name: Mapped[Optional[str]] = mapped_column(String(255))
    vehicle_journey_id: Mapped[Optional[int]] = mapped_column(Integer)
    stop_activity_id: Mapped[Optional[int]] = mapped_column(Integer)
    auto_sequence_number: Mapped[Optional[int]] = mapped_column(Integer)

    stop_activity: Mapped[Optional['TransmodelStopactivity']] = relationship('TransmodelStopactivity', back_populates='transmodel_servicepatternstop')
    vehicle_journey: Mapped[Optional['TransmodelVehiclejourney']] = relationship('TransmodelVehiclejourney', back_populates='transmodel_servicepatternstop')
    data_quality_observationresults: Mapped[List['DataQualityObservationresults']] = relationship('DataQualityObservationresults', back_populates='service_pattern_stop')
    dqs_observationresults: Mapped[List['DqsObservationresults']] = relationship('DqsObservationresults', back_populates='service_pattern_stop')
    organisation_consumerfeedback: Mapped[List['OrganisationConsumerfeedback']] = relationship('OrganisationConsumerfeedback', back_populates='service_pattern_stop')


class TransmodelTracksvehiclejourney(Base):
    __tablename__ = 'transmodel_tracksvehiclejourney'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    tracks_id: Mapped[int] = mapped_column(Integer)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)
    sequence_number: Mapped[Optional[int]] = mapped_column(Integer)

    tracks: Mapped['TransmodelTracks'] = relationship('TransmodelTracks', back_populates='transmodel_tracksvehiclejourney')
    vehicle_journey: Mapped['TransmodelVehiclejourney'] = relationship('TransmodelVehiclejourney', back_populates='transmodel_tracksvehiclejourney')


class UsersAgentuserinvite(Base):
    __tablename__ = 'users_agentuserinvite'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String(50))
    inviter_id: Mapped[int] = mapped_column(Integer)
    organisation_id: Mapped[int] = mapped_column(Integer)
    agent_id: Mapped[Optional[int]] = mapped_column(Integer)
    invitation_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    agent: Mapped[Optional['UsersUser']] = relationship('UsersUser', back_populates='users_agentuserinvite')
    invitation: Mapped[Optional['UsersInvitation']] = relationship('UsersInvitation', back_populates='users_agentuserinvite')
    inviter: Mapped['UsersUser'] = relationship('UsersUser', back_populates='users_agentuserinvite_')
    organisation: Mapped['OrganisationOrganisation'] = relationship('OrganisationOrganisation', back_populates='users_agentuserinvite')


class DataQualityObservationresults(Base):
    __tablename__ = 'data_quality_observationresults'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    details: Mapped[str] = mapped_column(Text)
    service_pattern_stop_id: Mapped[int] = mapped_column(Integer)
    taskresults_id: Mapped[int] = mapped_column(Integer)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)

    service_pattern_stop: Mapped['TransmodelServicepatternstop'] = relationship('TransmodelServicepatternstop', back_populates='data_quality_observationresults')
    taskresults: Mapped['DataQualityTaskresults'] = relationship('DataQualityTaskresults', back_populates='data_quality_observationresults')
    vehicle_journey: Mapped['TransmodelVehiclejourney'] = relationship('TransmodelVehiclejourney', back_populates='data_quality_observationresults')


class DqsObservationresults(Base):
    __tablename__ = 'dqs_observationresults'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    details: Mapped[str] = mapped_column(Text)
    taskresults_id: Mapped[int] = mapped_column(Integer)
    service_pattern_stop_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    vehicle_journey_id: Mapped[Optional[int]] = mapped_column(Integer)
    is_suppressed: Mapped[Optional[bool]] = mapped_column(Boolean)
    serviced_organisation_vehicle_journey_id: Mapped[Optional[int]] = mapped_column(Integer)

    service_pattern_stop: Mapped[Optional['TransmodelServicepatternstop']] = relationship('TransmodelServicepatternstop', back_populates='dqs_observationresults')
    serviced_organisation_vehicle_journey: Mapped[Optional['TransmodelServicedorganisationvehiclejourney']] = relationship('TransmodelServicedorganisationvehiclejourney', back_populates='dqs_observationresults')
    taskresults: Mapped['DqsTaskresults'] = relationship('DqsTaskresults', back_populates='dqs_observationresults')
    vehicle_journey: Mapped[Optional['TransmodelVehiclejourney']] = relationship('TransmodelVehiclejourney', back_populates='dqs_observationresults')


class NaptanFlexiblezone(Base):
    __tablename__ = 'naptan_flexiblezone'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    sequence_number: Mapped[int] = mapped_column(Integer)
    location: Mapped[Any] = mapped_column(Geometry('POINT', 4326, from_text='ST_GeomFromEWKT', name='geometry', nullable=False))
    naptan_stoppoint_id: Mapped[int] = mapped_column(Integer)

    naptan_stoppoint: Mapped['NaptanStoppoint'] = relationship('NaptanStoppoint', back_populates='naptan_flexiblezone')


class OrganisationConsumerfeedback(Base):
    __tablename__ = 'organisation_consumerfeedback'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    feedback: Mapped[str] = mapped_column(Text)
    organisation_id: Mapped[int] = mapped_column(Integer)
    consumer_id: Mapped[Optional[int]] = mapped_column(Integer)
    dataset_id: Mapped[Optional[int]] = mapped_column(Integer)
    is_suppressed: Mapped[Optional[bool]] = mapped_column(Boolean)
    revision_id: Mapped[Optional[int]] = mapped_column(Integer)
    service_id: Mapped[Optional[int]] = mapped_column(Integer)
    service_pattern_stop_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    vehicle_journey_id: Mapped[Optional[int]] = mapped_column(Integer)
    service_pattern_id: Mapped[Optional[int]] = mapped_column(Integer)

    consumer: Mapped[Optional['UsersUser']] = relationship('UsersUser', back_populates='organisation_consumerfeedback')
    dataset: Mapped[Optional['OrganisationDataset']] = relationship('OrganisationDataset', back_populates='organisation_consumerfeedback')
    organisation: Mapped['OrganisationOrganisation'] = relationship('OrganisationOrganisation', back_populates='organisation_consumerfeedback')
    revision: Mapped[Optional['OrganisationDatasetrevision']] = relationship('OrganisationDatasetrevision', back_populates='organisation_consumerfeedback')
    service: Mapped[Optional['TransmodelService']] = relationship('TransmodelService', back_populates='organisation_consumerfeedback')
    service_pattern: Mapped[Optional['TransmodelServicepattern']] = relationship('TransmodelServicepattern', back_populates='organisation_consumerfeedback')
    service_pattern_stop: Mapped[Optional['TransmodelServicepatternstop']] = relationship('TransmodelServicepatternstop', back_populates='organisation_consumerfeedback')
    vehicle_journey: Mapped[Optional['TransmodelVehiclejourney']] = relationship('TransmodelVehiclejourney', back_populates='organisation_consumerfeedback')


class TransmodelServicedorganisationworkingdays(Base):
    __tablename__ = 'transmodel_servicedorganisationworkingdays'

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    start_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    serviced_organisation_vehicle_journey_id: Mapped[Optional[int]] = mapped_column(Integer)

    serviced_organisation_vehicle_journey: Mapped[Optional['TransmodelServicedorganisationvehiclejourney']] = relationship('TransmodelServicedorganisationvehiclejourney', back_populates='transmodel_servicedorganisationworkingdays')
