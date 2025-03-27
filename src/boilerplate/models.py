from typing import Any, List, Optional

from geoalchemy2.types import Geometry
from sqlalchemy import ARRAY, BigInteger, Boolean, CheckConstraint, Date, DateTime, ForeignKeyConstraint, Identity, Index, Integer, PrimaryKeyConstraint, String, Text, Time, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship
import datetime

class Base(MappedAsDataclass, DeclarativeBase):
    pass


class DqsChecks(Base):
    __tablename__ = 'dqs_checks'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='dqs_checks_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    observation: Mapped[str] = mapped_column(String(1024))
    importance: Mapped[str] = mapped_column(String(64))
    category: Mapped[str] = mapped_column(String(64))
    queue_name: Mapped[Optional[str]] = mapped_column(String(256))

    dqs_taskresults: Mapped[List['DqsTaskresults']] = relationship('DqsTaskresults', back_populates='checks')


class NaptanDistrict(Base):
    __tablename__ = 'naptan_district'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='naptan_district_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    naptan_locality: Mapped[List['NaptanLocality']] = relationship('NaptanLocality', back_populates='district')


class OrganisationDataset(Base):
    __tablename__ = 'organisation_dataset'
    __table_args__ = (
        ForeignKeyConstraint(['contact_id'], ['public.users_user.id'], deferrable=True, initially='DEFERRED', name='organisation_dataset_contact_id_b440c22b_fk_users_user_id'),
        ForeignKeyConstraint(['live_revision_id'], ['public.organisation_datasetrevision.id'], deferrable=True, initially='DEFERRED', name='organisation_dataset_live_revision_id_e30c3fa4_fk_organisat'),
        ForeignKeyConstraint(['organisation_id'], ['public.organisation_organisation.id'], deferrable=True, initially='DEFERRED', name='organisation_dataset_organisation_id_384c7a11_fk_organisat'),
        PrimaryKeyConstraint('id', name='organisation_dataset_pkey'),
        UniqueConstraint('live_revision_id', name='organisation_dataset_live_revision_id_key'),
        Index('organisation_dataset_contact_id_b440c22b', 'contact_id'),
        Index('organisation_dataset_organisation_id_384c7a11', 'organisation_id'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
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
    live_revision: Mapped[Optional['OrganisationDatasetrevision']] = relationship('OrganisationDatasetrevision', foreign_keys=[live_revision_id], back_populates='organisation_dataset')
    organisation: Mapped['OrganisationOrganisation'] = relationship('OrganisationOrganisation', back_populates='organisation_dataset')
    organisation_datasetrevision: Mapped[List['OrganisationDatasetrevision']] = relationship('OrganisationDatasetrevision', foreign_keys='[OrganisationDatasetrevision.dataset_id]', back_populates='dataset')


class OrganisationDatasetrevision(Base):
    __tablename__ = 'organisation_datasetrevision'
    __table_args__ = (
        CheckConstraint('num_of_bus_stops >= 0', name='organisation_datasetrevision_num_of_bus_stops_check'),
        CheckConstraint('num_of_lines >= 0', name='organisation_datasetrevision_num_of_lines_check'),
        CheckConstraint('num_of_operators >= 0', name='organisation_datasetrevision_num_of_operators_check'),
        CheckConstraint('num_of_timing_points >= 0', name='organisation_datasetrevision_num_of_timing_points_check'),
        ForeignKeyConstraint(['dataset_id'], ['public.organisation_dataset.id'], deferrable=True, initially='DEFERRED', name='organisation_dataset_dataset_id_f0cd70df_fk_organisat'),
        ForeignKeyConstraint(['last_modified_user_id'], ['public.users_user.id'], deferrable=True, initially='DEFERRED', name='organisation_dataset_last_modified_user_i_cfda7737_fk_users_use'),
        ForeignKeyConstraint(['published_by_id'], ['public.users_user.id'], deferrable=True, initially='DEFERRED', name='organisation_dataset_published_by_id_4e5c02d1_fk_users_use'),
        PrimaryKeyConstraint('id', name='organisation_datasetrevision_pkey'),
        UniqueConstraint('dataset_id', 'created', name='organisation_datasetrevision_unique_revision'),
        UniqueConstraint('name', name='organisation_datasetrevision_name_24f6c4c0_uniq'),
        Index('organisatio_is_publ_bee2ff_idx', 'is_published'),
        Index('organisation_datasetrevision_dataset_id_f0cd70df', 'dataset_id'),
        Index('organisation_datasetrevision_last_modified_user_id_cfda7737', 'last_modified_user_id'),
        Index('organisation_datasetrevision_name_24f6c4c0_like', 'name'),
        Index('organisation_datasetrevision_published_by_id_4e5c02d1', 'published_by_id'),
        Index('organisation_datasetrevision_unique_draft_revision', 'dataset_id', unique=True),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
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

    organisation_dataset: Mapped[Optional['OrganisationDataset']] = relationship('OrganisationDataset', uselist=False, foreign_keys='[OrganisationDataset.live_revision_id]', back_populates='live_revision')
    dataset: Mapped['OrganisationDataset'] = relationship('OrganisationDataset', foreign_keys=[dataset_id], back_populates='organisation_datasetrevision')
    last_modified_user: Mapped[Optional['UsersUser']] = relationship('UsersUser', foreign_keys=[last_modified_user_id], back_populates='organisation_datasetrevision')
    published_by: Mapped[Optional['UsersUser']] = relationship('UsersUser', foreign_keys=[published_by_id], back_populates='organisation_datasetrevision_')
    dqs_report: Mapped[List['DqsReport']] = relationship('DqsReport', back_populates='revision')
    organisation_txcfileattributes: Mapped[List['OrganisationTxcfileattributes']] = relationship('OrganisationTxcfileattributes', back_populates='revision')
    transmodel_servicepattern: Mapped[List['TransmodelServicepattern']] = relationship('TransmodelServicepattern', back_populates='revision')


class TransmodelServicedorganisations(Base):
    __tablename__ = 'transmodel_servicedorganisations'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='transmodel_servicedorganisations_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    organisation_code: Mapped[Optional[str]] = mapped_column(String(255))

    transmodel_servicedorganisationvehiclejourney: Mapped[List['TransmodelServicedorganisationvehiclejourney']] = relationship('TransmodelServicedorganisationvehiclejourney', back_populates='serviced_organisation')


class TransmodelStopactivity(Base):
    __tablename__ = 'transmodel_stopactivity'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='transmodel_stopactivity_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    is_pickup: Mapped[bool] = mapped_column(Boolean)
    is_setdown: Mapped[bool] = mapped_column(Boolean)
    is_driverrequest: Mapped[bool] = mapped_column(Boolean)

    transmodel_servicepatternstop: Mapped[List['TransmodelServicepatternstop']] = relationship('TransmodelServicepatternstop', back_populates='stop_activity')


class UiLta(Base):
    __tablename__ = 'ui_lta'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='ui_lta_pkey'),
        UniqueConstraint('id', 'name', name='ui_lta_id_name_304a2476_uniq'),
        UniqueConstraint('name', name='ui_lta_name_key'),
        Index('ui_lta_name_8bea4104_like', 'name'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    avl_sra: Mapped[Optional[int]] = mapped_column(Integer)
    fares_sra: Mapped[Optional[int]] = mapped_column(Integer)
    overall_sra: Mapped[Optional[int]] = mapped_column(Integer)
    timetable_sra: Mapped[Optional[int]] = mapped_column(Integer)
    total_inscope: Mapped[Optional[int]] = mapped_column(Integer)

    naptan_adminarea: Mapped[List['NaptanAdminarea']] = relationship('NaptanAdminarea', back_populates='ui_lta')


class UsersUser(Base):
    __tablename__ = 'users_user'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_user_pkey'),
        UniqueConstraint('username', name='users_user_username_key'),
        Index('users_user_username_06e46fe6_like', 'username'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
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
    organisation_datasetrevision: Mapped[List['OrganisationDatasetrevision']] = relationship('OrganisationDatasetrevision', foreign_keys='[OrganisationDatasetrevision.last_modified_user_id]', back_populates='last_modified_user')
    organisation_datasetrevision_: Mapped[List['OrganisationDatasetrevision']] = relationship('OrganisationDatasetrevision', foreign_keys='[OrganisationDatasetrevision.published_by_id]', back_populates='published_by')
    organisation_organisation: Mapped[Optional['OrganisationOrganisation']] = relationship('OrganisationOrganisation', uselist=False, back_populates='key_contact')


class DqsReport(Base):
    __tablename__ = 'dqs_report'
    __table_args__ = (
        ForeignKeyConstraint(['revision_id'], ['public.organisation_datasetrevision.id'], deferrable=True, initially='DEFERRED', name='dqs_report_revision_id_6eda8a8d_fk_organisat'),
        PrimaryKeyConstraint('id', name='dqs_report_pkey'),
        Index('dqs_report_revision_id_6eda8a8d', 'revision_id'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    file_name: Mapped[str] = mapped_column(String(255))
    revision_id: Mapped[int] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(String(64))

    revision: Mapped['OrganisationDatasetrevision'] = relationship('OrganisationDatasetrevision', back_populates='dqs_report')
    dqs_taskresults: Mapped[List['DqsTaskresults']] = relationship('DqsTaskresults', back_populates='dataquality_report')


class NaptanAdminarea(Base):
    __tablename__ = 'naptan_adminarea'
    __table_args__ = (
        ForeignKeyConstraint(['ui_lta_id'], ['public.ui_lta.id'], deferrable=True, initially='DEFERRED', name='naptan_adminarea_ui_lta_id_c37d8a17_fk_ui_lta_id'),
        PrimaryKeyConstraint('id', name='naptan_adminarea_pkey'),
        UniqueConstraint('atco_code', name='naptan_adminarea_atco_code_key'),
        Index('naptan_adminarea_atco_code_167e083c_like', 'atco_code'),
        Index('naptan_adminarea_ui_lta_id_c37d8a17', 'ui_lta_id'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    traveline_region_id: Mapped[str] = mapped_column(String(255))
    atco_code: Mapped[str] = mapped_column(String(255))
    ui_lta_id: Mapped[Optional[int]] = mapped_column(Integer)

    ui_lta: Mapped[Optional['UiLta']] = relationship('UiLta', back_populates='naptan_adminarea')
    naptan_locality: Mapped[List['NaptanLocality']] = relationship('NaptanLocality', back_populates='admin_area')
    naptan_stoppoint: Mapped[List['NaptanStoppoint']] = relationship('NaptanStoppoint', back_populates='admin_area')


class OrganisationOrganisation(Base):
    __tablename__ = 'organisation_organisation'
    __table_args__ = (
        ForeignKeyConstraint(['key_contact_id'], ['public.users_user.id'], deferrable=True, initially='DEFERRED', name='organisation_organis_key_contact_id_df58d4ce_fk_users_use'),
        PrimaryKeyConstraint('id', name='organisation_organisation_pkey'),
        UniqueConstraint('key_contact_id', name='organisation_organisation_key_contact_id_key'),
        UniqueConstraint('name', name='organisation_organisation_name_6b81abae_uniq'),
        Index('organisation_name_idx', 'name'),
        Index('organisation_organisation_name_6b81abae_like', 'name'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
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
    organisation_operatorcode: Mapped[List['OrganisationOperatorcode']] = relationship('OrganisationOperatorcode', back_populates='organisation')


class OrganisationTxcfileattributes(Base):
    __tablename__ = 'organisation_txcfileattributes'
    __table_args__ = (
        ForeignKeyConstraint(['revision_id'], ['public.organisation_datasetrevision.id'], deferrable=True, initially='DEFERRED', name='organisation_txcfile_revision_id_ddb2f841_fk_organisat'),
        PrimaryKeyConstraint('id', name='organisation_txcfileattributes_pkey'),
        Index('organisation_txcfileattributes_revision_id_ddb2f841', 'revision_id'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
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
    dqs_taskresults: Mapped[List['DqsTaskresults']] = relationship('DqsTaskresults', back_populates='transmodel_txcfileattributes')


class TransmodelServicepattern(Base):
    __tablename__ = 'transmodel_servicepattern'
    __table_args__ = (
        ForeignKeyConstraint(['revision_id'], ['public.organisation_datasetrevision.id'], deferrable=True, initially='DEFERRED', name='transmodel_servicepa_revision_id_6917ba40_fk_organisat'),
        PrimaryKeyConstraint('id', name='transmodel_servicepattern_pkey'),
        Index('transmodel_servicepattern_geom_72c24c56_id', 'geom'),
        Index('transmodel_servicepattern_line_name_b3fc6144', 'line_name'),
        Index('transmodel_servicepattern_line_name_b3fc6144_like', 'line_name'),
        Index('transmodel_servicepattern_revision_id_6917ba40', 'revision_id'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    service_pattern_id: Mapped[str] = mapped_column(String(255))
    origin: Mapped[str] = mapped_column(String(255))
    destination: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    geom: Mapped[Optional[Any]] = mapped_column(Geometry('LINESTRING', 4326, from_text='ST_GeomFromEWKT', name='geometry'))
    revision_id: Mapped[Optional[int]] = mapped_column(Integer)
    line_name: Mapped[Optional[str]] = mapped_column(String(255))

    revision: Mapped[Optional['OrganisationDatasetrevision']] = relationship('OrganisationDatasetrevision', back_populates='transmodel_servicepattern')
    transmodel_vehiclejourney: Mapped[List['TransmodelVehiclejourney']] = relationship('TransmodelVehiclejourney', back_populates='service_pattern')
    transmodel_servicepatternstop: Mapped[List['TransmodelServicepatternstop']] = relationship('TransmodelServicepatternstop', back_populates='service_pattern')


class DqsTaskresults(Base):
    __tablename__ = 'dqs_taskresults'
    __table_args__ = (
        ForeignKeyConstraint(['checks_id'], ['public.dqs_checks.id'], deferrable=True, initially='DEFERRED', name='dqs_taskresults_checks_id_a474fbd2_fk_dqs_checks_id'),
        ForeignKeyConstraint(['dataquality_report_id'], ['public.dqs_report.id'], deferrable=True, initially='DEFERRED', name='dqs_taskresults_dataquality_report_id_b3cfb422_fk_dqs_report_id'),
        ForeignKeyConstraint(['transmodel_txcfileattributes_id'], ['public.organisation_txcfileattributes.id'], deferrable=True, initially='DEFERRED', name='dqs_taskresults_transmodel_txcfileat_36d8a29c_fk_organisat'),
        PrimaryKeyConstraint('id', name='dqs_taskresults_pkey'),
        Index('dqs_taskresults_checks_id_a474fbd2', 'checks_id'),
        Index('dqs_taskresults_dataquality_report_id_b3cfb422', 'dataquality_report_id'),
        Index('dqs_taskresults_transmodel_txcfileattributes_id_36d8a29c', 'transmodel_txcfileattributes_id'),
        {'schema': 'public'}
    )

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


class NaptanLocality(Base):
    __tablename__ = 'naptan_locality'
    __table_args__ = (
        ForeignKeyConstraint(['admin_area_id'], ['public.naptan_adminarea.id'], deferrable=True, initially='DEFERRED', name='naptan_locality_admin_area_id_0765cd72_fk_naptan_adminarea_id'),
        ForeignKeyConstraint(['district_id'], ['public.naptan_district.id'], deferrable=True, initially='DEFERRED', name='naptan_locality_district_id_39815ea9_fk_naptan_district_id'),
        PrimaryKeyConstraint('gazetteer_id', name='naptan_locality_pkey'),
        Index('naptan_locality_admin_area_id_0765cd72', 'admin_area_id'),
        Index('naptan_locality_district_id_39815ea9', 'district_id'),
        Index('naptan_locality_gazetteer_id_6170fc8e_like', 'gazetteer_id'),
        {'schema': 'public'}
    )

    gazetteer_id: Mapped[str] = mapped_column(String(8), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    easting: Mapped[int] = mapped_column(Integer)
    northing: Mapped[int] = mapped_column(Integer)
    admin_area_id: Mapped[Optional[int]] = mapped_column(Integer)
    district_id: Mapped[Optional[int]] = mapped_column(Integer)

    admin_area: Mapped[Optional['NaptanAdminarea']] = relationship('NaptanAdminarea', back_populates='naptan_locality')
    district: Mapped[Optional['NaptanDistrict']] = relationship('NaptanDistrict', back_populates='naptan_locality')
    naptan_stoppoint: Mapped[List['NaptanStoppoint']] = relationship('NaptanStoppoint', back_populates='locality')


class OrganisationOperatorcode(Base):
    __tablename__ = 'organisation_operatorcode'
    __table_args__ = (
        ForeignKeyConstraint(['organisation_id'], ['public.organisation_organisation.id'], deferrable=True, initially='DEFERRED', name='organisation_operato_organisation_id_854edcec_fk_organisat'),
        PrimaryKeyConstraint('id', name='organisation_operatorcode_pkey'),
        UniqueConstraint('noc', name='organisation_operatorcode_noc_d6b5203e_uniq'),
        Index('organisation_operatorcode_noc_d6b5203e_like', 'noc'),
        Index('organisation_operatorcode_organisation_id_854edcec', 'organisation_id'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    noc: Mapped[str] = mapped_column(String(20))
    organisation_id: Mapped[int] = mapped_column(Integer)

    organisation: Mapped['OrganisationOrganisation'] = relationship('OrganisationOrganisation', back_populates='organisation_operatorcode')


class TransmodelVehiclejourney(Base):
    __tablename__ = 'transmodel_vehiclejourney'
    __table_args__ = (
        ForeignKeyConstraint(['service_pattern_id'], ['public.transmodel_servicepattern.id'], deferrable=True, initially='DEFERRED', name='transmodel_vehiclejo_service_pattern_id_1b8caece_fk_transmode'),
        PrimaryKeyConstraint('id', name='transmodel_vehiclejourney_pkey'),
        Index('transmodel_vehiclejourney_service_pattern_id_1b8caece', 'service_pattern_id'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    departure_day_shift: Mapped[bool] = mapped_column(Boolean)
    start_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    direction: Mapped[Optional[str]] = mapped_column(String(255))
    journey_code: Mapped[Optional[str]] = mapped_column(String(255))
    line_ref: Mapped[Optional[str]] = mapped_column(String(255))
    service_pattern_id: Mapped[Optional[int]] = mapped_column(Integer)
    block_number: Mapped[Optional[str]] = mapped_column(String(20))

    service_pattern: Mapped[Optional['TransmodelServicepattern']] = relationship('TransmodelServicepattern', back_populates='transmodel_vehiclejourney')
    transmodel_servicedorganisationvehiclejourney: Mapped[List['TransmodelServicedorganisationvehiclejourney']] = relationship('TransmodelServicedorganisationvehiclejourney', back_populates='vehicle_journey')
    transmodel_servicepatternstop: Mapped[List['TransmodelServicepatternstop']] = relationship('TransmodelServicepatternstop', back_populates='vehicle_journey')
    dqs_observationresults: Mapped[List['DqsObservationresults']] = relationship('DqsObservationresults', back_populates='vehicle_journey')


class NaptanStoppoint(Base):
    __tablename__ = 'naptan_stoppoint'
    __table_args__ = (
        ForeignKeyConstraint(['admin_area_id'], ['public.naptan_adminarea.id'], deferrable=True, initially='DEFERRED', name='naptan_stoppoint_admin_area_id_6ccac623_fk_naptan_adminarea_id'),
        ForeignKeyConstraint(['locality_id'], ['public.naptan_locality.gazetteer_id'], deferrable=True, initially='DEFERRED', name='naptan_stoppoint_locality_id_4ef6e016_fk_naptan_lo'),
        PrimaryKeyConstraint('id', name='naptan_stoppoint_pkey'),
        UniqueConstraint('atco_code', name='naptan_stoppoint_atco_code_key'),
        Index('naptan_stoppoint_admin_area_id_6ccac623', 'admin_area_id'),
        Index('naptan_stoppoint_atco_code_b99b7c43_like', 'atco_code'),
        Index('naptan_stoppoint_locality_id_4ef6e016', 'locality_id'),
        Index('naptan_stoppoint_locality_id_4ef6e016_like', 'locality_id'),
        Index('naptan_stoppoint_location_741ad66c_id', 'location'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
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
    transmodel_servicepatternstop: Mapped[List['TransmodelServicepatternstop']] = relationship('TransmodelServicepatternstop', back_populates='naptan_stop')


class TransmodelServicedorganisationvehiclejourney(Base):
    __tablename__ = 'transmodel_servicedorganisationvehiclejourney'
    __table_args__ = (
        ForeignKeyConstraint(['serviced_organisation_id'], ['public.transmodel_servicedorganisations.id'], deferrable=True, initially='DEFERRED', name='transmodel_servicedo_serviced_organisatio_4f5b7f54_fk_transmode'),
        ForeignKeyConstraint(['vehicle_journey_id'], ['public.transmodel_vehiclejourney.id'], deferrable=True, initially='DEFERRED', name='transmodel_servicedo_vehicle_journey_id_da3adc3a_fk_transmode'),
        PrimaryKeyConstraint('id', name='transmodel_servicedorganisationvehiclejourney_pkey'),
        Index('transmodel_servicedorganis_serviced_organisation_id_4f5b7f54', 'serviced_organisation_id'),
        Index('transmodel_servicedorganis_vehicle_journey_id_da3adc3a', 'vehicle_journey_id'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    operating_on_working_days: Mapped[bool] = mapped_column(Boolean)
    serviced_organisation_id: Mapped[int] = mapped_column(Integer)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)

    serviced_organisation: Mapped['TransmodelServicedorganisations'] = relationship('TransmodelServicedorganisations', back_populates='transmodel_servicedorganisationvehiclejourney')
    vehicle_journey: Mapped['TransmodelVehiclejourney'] = relationship('TransmodelVehiclejourney', back_populates='transmodel_servicedorganisationvehiclejourney')
    dqs_observationresults: Mapped[List['DqsObservationresults']] = relationship('DqsObservationresults', back_populates='serviced_organisation_vehicle_journey')


class TransmodelServicepatternstop(Base):
    __tablename__ = 'transmodel_servicepatternstop'
    __table_args__ = (
        ForeignKeyConstraint(['naptan_stop_id'], ['public.naptan_stoppoint.id'], deferrable=True, initially='DEFERRED', name='transmodel_servicepa_naptan_stop_id_e9dd8eac_fk_naptan_st'),
        ForeignKeyConstraint(['service_pattern_id'], ['public.transmodel_servicepattern.id'], deferrable=True, initially='DEFERRED', name='transmodel_servicepa_service_pattern_id_c78a2156_fk_transmode'),
        ForeignKeyConstraint(['stop_activity_id'], ['public.transmodel_stopactivity.id'], deferrable=True, initially='DEFERRED', name='transmodel_servicepa_stop_activity_id_cd96c52d_fk_transmode'),
        ForeignKeyConstraint(['vehicle_journey_id'], ['public.transmodel_vehiclejourney.id'], deferrable=True, initially='DEFERRED', name='transmodel_servicepa_vehicle_journey_id_32f3f1c9_fk_transmode'),
        PrimaryKeyConstraint('id', name='transmodel_servicepatternstop_pkey'),
        Index('transmodel_servicepatternstop_naptan_stop_id_e9dd8eac', 'naptan_stop_id'),
        Index('transmodel_servicepatternstop_service_pattern_id_c78a2156', 'service_pattern_id'),
        Index('transmodel_servicepatternstop_stop_activity_id_cd96c52d', 'stop_activity_id'),
        Index('transmodel_servicepatternstop_vehicle_journey_id_32f3f1c9', 'vehicle_journey_id'),
        {'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
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

    naptan_stop: Mapped[Optional['NaptanStoppoint']] = relationship('NaptanStoppoint', back_populates='transmodel_servicepatternstop')
    service_pattern: Mapped['TransmodelServicepattern'] = relationship('TransmodelServicepattern', back_populates='transmodel_servicepatternstop')
    stop_activity: Mapped[Optional['TransmodelStopactivity']] = relationship('TransmodelStopactivity', back_populates='transmodel_servicepatternstop')
    vehicle_journey: Mapped[Optional['TransmodelVehiclejourney']] = relationship('TransmodelVehiclejourney', back_populates='transmodel_servicepatternstop')
    dqs_observationresults: Mapped[List['DqsObservationresults']] = relationship('DqsObservationresults', back_populates='service_pattern_stop')


class DqsObservationresults(Base):
    __tablename__ = 'dqs_observationresults'
    __table_args__ = (
        ForeignKeyConstraint(['service_pattern_stop_id'], ['public.transmodel_servicepatternstop.id'], deferrable=True, initially='DEFERRED', name='dqs_observationresults_service_pattern_stop_id_603d0be8_fk'),
        ForeignKeyConstraint(['serviced_organisation_vehicle_journey_id'], ['public.transmodel_servicedorganisationvehiclejourney.id'], deferrable=True, initially='DEFERRED', name='dqs_observationresul_serviced_organisatio_b564ba8e_fk_transmode'),
        ForeignKeyConstraint(['taskresults_id'], ['public.dqs_taskresults.id'], deferrable=True, initially='DEFERRED', name='dqs_observationresul_taskresults_id_80858afc_fk_dqs_taskr'),
        ForeignKeyConstraint(['vehicle_journey_id'], ['public.transmodel_vehiclejourney.id'], deferrable=True, initially='DEFERRED', name='dqs_observationresul_vehicle_journey_id_6e76a0f9_fk_transmode'),
        PrimaryKeyConstraint('id', name='dqs_observationresults_pkey'),
        Index('dqs_observationresults_service_pattern_stop_id_603d0be8', 'service_pattern_stop_id'),
        Index('dqs_observationresults_serviced_organisation_vehi_b564ba8e', 'serviced_organisation_vehicle_journey_id'),
        Index('dqs_observationresults_taskresults_id_80858afc', 'taskresults_id'),
        Index('dqs_observationresults_vehicle_journey_id_6e76a0f9', 'vehicle_journey_id'),
        {'schema': 'public'}
    )

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
