from typing import Any, List, Optional

from geoalchemy2.types import Geometry
from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Double,
    ForeignKeyConstraint,
    Identity,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    Sequence,
    SmallInteger,
    String,
    Text,
    Time,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.dialects.postgresql import INTERVAL, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal
import uuid


class Base(DeclarativeBase):
    pass


class AuthGroup(Base):
    __tablename__ = "auth_group"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="auth_group_pkey"),
        UniqueConstraint("name", name="auth_group_name_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150))

    users_user_groups: Mapped[List["UsersUserGroups"]] = relationship(
        "UsersUserGroups", back_populates="group"
    )
    waffle_flag_groups: Mapped[List["WaffleFlagGroups"]] = relationship(
        "WaffleFlagGroups", back_populates="group"
    )
    auth_group_permissions: Mapped[List["AuthGroupPermissions"]] = relationship(
        "AuthGroupPermissions", back_populates="group"
    )


class AvlCavldataarchive(Base):
    __tablename__ = "avl_cavldataarchive"
    __table_args__ = (PrimaryKeyConstraint("id", name="avl_cavldataarchive_pkey"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    data: Mapped[str] = mapped_column(String(100))
    data_format: Mapped[str] = mapped_column(String(2))


class ChangelogHighlevelroadmap(Base):
    __tablename__ = "changelog_highlevelroadmap"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="changelog_highlevelroadmap_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    description: Mapped[str] = mapped_column(Text)


class ChangelogKnownissues(Base):
    __tablename__ = "changelog_knownissues"
    __table_args__ = (PrimaryKeyConstraint("id", name="changelog_knownissues_pkey"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20))
    deleted: Mapped[bool] = mapped_column(Boolean)


class DataQualityChecks(Base):
    __tablename__ = "data_quality_checks"
    __table_args__ = (PrimaryKeyConstraint("id", name="data_quality_checks_pkey"),)

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    observation: Mapped[str] = mapped_column(String(1024))
    importance: Mapped[str] = mapped_column(String(64))
    category: Mapped[str] = mapped_column(String(64))

    data_quality_taskresults: Mapped[List["DataQualityTaskresults"]] = relationship(
        "DataQualityTaskresults", back_populates="checks"
    )


class DataQualityService(Base):
    __tablename__ = "data_quality_service"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="data_quality_service_pkey"),
        UniqueConstraint("ito_id", name="data_quality_service_ito_id_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    ito_id: Mapped[str] = mapped_column(Text)

    data_quality_lineexpiredwarning: Mapped[List["DataQualityLineexpiredwarning"]] = (
        relationship("DataQualityLineexpiredwarning", back_populates="service")
    )
    data_quality_linemissingblockidwarning: Mapped[
        List["DataQualityLinemissingblockidwarning"]
    ] = relationship("DataQualityLinemissingblockidwarning", back_populates="service")
    data_quality_service_reports: Mapped[List["DataQualityServiceReports"]] = (
        relationship("DataQualityServiceReports", back_populates="service")
    )


class DataQualityServicepatternservicelink(Base):
    __tablename__ = "data_quality_servicepatternservicelink"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="data_quality_servicepatternservicelink_pkey"),
        UniqueConstraint(
            "service_pattern_id",
            "service_link_id",
            "position",
            name="data_quality_servicepatt_service_pattern_id_servi_2914dece_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position: Mapped[int] = mapped_column(Integer)
    service_link_id: Mapped[int] = mapped_column(Integer)
    service_pattern_id: Mapped[int] = mapped_column(Integer)


class DataQualityServicepatternstop(Base):
    __tablename__ = "data_quality_servicepatternstop"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="data_quality_servicepatternstop_pkey"),
        UniqueConstraint(
            "service_pattern_id",
            "stop_id",
            "position",
            name="data_quality_servicepatt_service_pattern_id_stop__fd1fd69a_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position: Mapped[int] = mapped_column(Integer)
    service_pattern_id: Mapped[int] = mapped_column(Integer)
    stop_id: Mapped[int] = mapped_column(Integer)

    data_quality_timingpatternstop: Mapped[List["DataQualityTimingpatternstop"]] = (
        relationship(
            "DataQualityTimingpatternstop", back_populates="service_pattern_stop"
        )
    )


class DataQualityTimingpattern(Base):
    __tablename__ = "data_quality_timingpattern"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="data_quality_timingpattern_pkey"),
        UniqueConstraint("ito_id", name="data_quality_timingpattern_ito_id_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_pattern_id: Mapped[int] = mapped_column(Integer)
    ito_id: Mapped[str] = mapped_column(Text)

    data_quality_timingpatternstop: Mapped[List["DataQualityTimingpatternstop"]] = (
        relationship("DataQualityTimingpatternstop", back_populates="timing_pattern")
    )
    data_quality_vehiclejourney: Mapped[List["DataQualityVehiclejourney"]] = (
        relationship("DataQualityVehiclejourney", back_populates="timing_pattern")
    )
    data_quality_fastlinkwarning: Mapped[List["DataQualityFastlinkwarning"]] = (
        relationship("DataQualityFastlinkwarning", back_populates="timing_pattern")
    )
    data_quality_fasttimingwarning: Mapped[List["DataQualityFasttimingwarning"]] = (
        relationship("DataQualityFasttimingwarning", back_populates="timing_pattern")
    )
    data_quality_slowlinkwarning: Mapped[List["DataQualitySlowlinkwarning"]] = (
        relationship("DataQualitySlowlinkwarning", back_populates="timing_pattern")
    )
    data_quality_slowtimingwarning: Mapped[List["DataQualitySlowtimingwarning"]] = (
        relationship("DataQualitySlowtimingwarning", back_populates="timing_pattern")
    )
    data_quality_timingbackwardswarning: Mapped[
        List["DataQualityTimingbackwardswarning"]
    ] = relationship(
        "DataQualityTimingbackwardswarning", back_populates="timing_pattern"
    )
    data_quality_timingdropoffwarning: Mapped[
        List["DataQualityTimingdropoffwarning"]
    ] = relationship("DataQualityTimingdropoffwarning", back_populates="timing_pattern")
    data_quality_timingfirstwarning: Mapped[List["DataQualityTimingfirstwarning"]] = (
        relationship("DataQualityTimingfirstwarning", back_populates="timing_pattern")
    )
    data_quality_timinglastwarning: Mapped[List["DataQualityTiminglastwarning"]] = (
        relationship("DataQualityTiminglastwarning", back_populates="timing_pattern")
    )
    data_quality_timingmissingpointwarning: Mapped[
        List["DataQualityTimingmissingpointwarning"]
    ] = relationship(
        "DataQualityTimingmissingpointwarning", back_populates="timing_pattern"
    )
    data_quality_timingmultiplewarning: Mapped[
        List["DataQualityTimingmultiplewarning"]
    ] = relationship(
        "DataQualityTimingmultiplewarning", back_populates="timing_pattern"
    )
    data_quality_timingpickupwarning: Mapped[List["DataQualityTimingpickupwarning"]] = (
        relationship("DataQualityTimingpickupwarning", back_populates="timing_pattern")
    )


class DisruptionsDisruptionsdataarchive(Base):
    __tablename__ = "disruptions_disruptionsdataarchive"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="disruptions_disruptionsdataarchive_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    data: Mapped[str] = mapped_column(String(100))


class DjangoCeleryBeatClockedschedule(Base):
    __tablename__ = "django_celery_beat_clockedschedule"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="django_celery_beat_clockedschedule_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clocked_time: Mapped[datetime.datetime] = mapped_column(DateTime(True))

    django_celery_beat_periodictask: Mapped[List["DjangoCeleryBeatPeriodictask"]] = (
        relationship("DjangoCeleryBeatPeriodictask", back_populates="clocked")
    )


class DjangoCeleryBeatCrontabschedule(Base):
    __tablename__ = "django_celery_beat_crontabschedule"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="django_celery_beat_crontabschedule_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    minute: Mapped[str] = mapped_column(String(240))
    hour: Mapped[str] = mapped_column(String(96))
    day_of_week: Mapped[str] = mapped_column(String(64))
    day_of_month: Mapped[str] = mapped_column(String(124))
    month_of_year: Mapped[str] = mapped_column(String(64))
    timezone: Mapped[str] = mapped_column(String(63))

    django_celery_beat_periodictask: Mapped[List["DjangoCeleryBeatPeriodictask"]] = (
        relationship("DjangoCeleryBeatPeriodictask", back_populates="crontab")
    )


class DjangoCeleryBeatIntervalschedule(Base):
    __tablename__ = "django_celery_beat_intervalschedule"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="django_celery_beat_intervalschedule_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    every: Mapped[int] = mapped_column(Integer)
    period: Mapped[str] = mapped_column(String(24))

    django_celery_beat_periodictask: Mapped[List["DjangoCeleryBeatPeriodictask"]] = (
        relationship("DjangoCeleryBeatPeriodictask", back_populates="interval")
    )


class DjangoCeleryBeatPeriodictasks(Base):
    __tablename__ = "django_celery_beat_periodictasks"
    __table_args__ = (
        PrimaryKeyConstraint("ident", name="django_celery_beat_periodictasks_pkey"),
    )

    ident: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    last_update: Mapped[datetime.datetime] = mapped_column(DateTime(True))


class DjangoCeleryBeatSolarschedule(Base):
    __tablename__ = "django_celery_beat_solarschedule"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="django_celery_beat_solarschedule_pkey"),
        UniqueConstraint(
            "event",
            "latitude",
            "longitude",
            name="django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event: Mapped[str] = mapped_column(String(24))
    latitude: Mapped[decimal.Decimal] = mapped_column(Numeric(9, 6))
    longitude: Mapped[decimal.Decimal] = mapped_column(Numeric(9, 6))

    django_celery_beat_periodictask: Mapped[List["DjangoCeleryBeatPeriodictask"]] = (
        relationship("DjangoCeleryBeatPeriodictask", back_populates="solar")
    )


class DjangoCeleryResultsChordcounter(Base):
    __tablename__ = "django_celery_results_chordcounter"
    __table_args__ = (
        CheckConstraint(
            "count >= 0", name="django_celery_results_chordcounter_count_check"
        ),
        PrimaryKeyConstraint("id", name="django_celery_results_chordcounter_pkey"),
        UniqueConstraint(
            "group_id", name="django_celery_results_chordcounter_group_id_key"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[str] = mapped_column(String(255))
    sub_tasks: Mapped[str] = mapped_column(Text)
    count: Mapped[int] = mapped_column(Integer)


class DjangoCeleryResultsGroupresult(Base):
    __tablename__ = "django_celery_results_groupresult"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="django_celery_results_groupresult_pkey"),
        UniqueConstraint(
            "group_id", name="django_celery_results_groupresult_group_id_key"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[str] = mapped_column(String(255))
    date_created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    date_done: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    content_type: Mapped[str] = mapped_column(String(128))
    content_encoding: Mapped[str] = mapped_column(String(64))
    result: Mapped[Optional[str]] = mapped_column(Text)


class DjangoCeleryResultsTaskresult(Base):
    __tablename__ = "django_celery_results_taskresult"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="django_celery_results_taskresult_pkey"),
        UniqueConstraint(
            "task_id", name="django_celery_results_taskresult_task_id_key"
        ),
    )

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
    __tablename__ = "django_content_type"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="django_content_type_pkey"),
        UniqueConstraint(
            "app_label",
            "model",
            name="django_content_type_app_label_model_76bd3d3b_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    app_label: Mapped[str] = mapped_column(String(100))
    model: Mapped[str] = mapped_column(String(100))

    auth_permission: Mapped[List["AuthPermission"]] = relationship(
        "AuthPermission", back_populates="content_type"
    )
    django_admin_log: Mapped[List["DjangoAdminLog"]] = relationship(
        "DjangoAdminLog", back_populates="content_type"
    )


class DjangoMigrations(Base):
    __tablename__ = "django_migrations"
    __table_args__ = (PrimaryKeyConstraint("id", name="django_migrations_pkey"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    app: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    applied: Mapped[datetime.datetime] = mapped_column(DateTime(True))


class DjangoSession(Base):
    __tablename__ = "django_session"
    __table_args__ = (PrimaryKeyConstraint("session_key", name="django_session_pkey"),)

    session_key: Mapped[str] = mapped_column(String(40), primary_key=True)
    session_data: Mapped[str] = mapped_column(Text)
    expire_date: Mapped[datetime.datetime] = mapped_column(DateTime(True))


class DjangoSite(Base):
    __tablename__ = "django_site"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="django_site_pkey"),
        UniqueConstraint("domain", name="django_site_domain_a2e37b91_uniq"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    domain: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(50))


class DqsChecks(Base):
    __tablename__ = "dqs_checks"
    __table_args__ = (PrimaryKeyConstraint("id", name="dqs_checks_pkey"),)

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    observation: Mapped[str] = mapped_column(String(1024))
    importance: Mapped[str] = mapped_column(String(64))
    category: Mapped[str] = mapped_column(String(64))
    queue_name: Mapped[Optional[str]] = mapped_column(String(256))

    dqs_taskresults: Mapped[List["DqsTaskresults"]] = relationship(
        "DqsTaskresults", back_populates="checks"
    )


class FeedbackFeedback(Base):
    __tablename__ = "feedback_feedback"
    __table_args__ = (PrimaryKeyConstraint("id", name="feedback_feedback_pkey"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date)
    page_url: Mapped[str] = mapped_column(String(2048))
    satisfaction_rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(String(1200))


class NaptanDistrict(Base):
    __tablename__ = "naptan_district"
    __table_args__ = (PrimaryKeyConstraint("id", name="naptan_district_pkey"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    naptan_locality: Mapped[List["NaptanLocality"]] = relationship(
        "NaptanLocality", back_populates="district"
    )


class OrganisationDataset(Base):
    __tablename__ = "organisation_dataset"
    __table_args__ = (
        ForeignKeyConstraint(
            ["contact_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_dataset_contact_id_b440c22b_fk_users_user_id",
        ),
        ForeignKeyConstraint(
            ["live_revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_dataset_live_revision_id_e30c3fa4_fk_organisat",
        ),
        ForeignKeyConstraint(
            ["organisation_id"],
            ["organisation_organisation.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_dataset_organisation_id_384c7a11_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="organisation_dataset_pkey"),
        UniqueConstraint(
            "live_revision_id", name="organisation_dataset_live_revision_id_key"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    organisation_id: Mapped[int] = mapped_column(Integer)
    contact_id: Mapped[int] = mapped_column(Integer)
    dataset_type: Mapped[int] = mapped_column(Integer)
    avl_feed_status: Mapped[str] = mapped_column(String(20))
    is_dummy: Mapped[bool] = mapped_column(Boolean)
    live_revision_id: Mapped[Optional[int]] = mapped_column(Integer)
    avl_feed_last_checked: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True)
    )

    contact: Mapped["UsersUser"] = relationship(
        "UsersUser", back_populates="organisation_dataset"
    )
    live_revision: Mapped[Optional["OrganisationDatasetrevision"]] = relationship(
        "OrganisationDatasetrevision",
        foreign_keys=[live_revision_id],
        back_populates="organisation_dataset",
    )
    organisation: Mapped["OrganisationOrganisation"] = relationship(
        "OrganisationOrganisation", back_populates="organisation_dataset"
    )
    organisation_datasetrevision: Mapped[List["OrganisationDatasetrevision"]] = (
        relationship(
            "OrganisationDatasetrevision",
            foreign_keys="[OrganisationDatasetrevision.dataset_id]",
            back_populates="dataset",
        )
    )
    avl_postpublishingcheckreport: Mapped[List["AvlPostpublishingcheckreport"]] = (
        relationship("AvlPostpublishingcheckreport", back_populates="dataset")
    )
    organisation_avlcompliancecache: Mapped["OrganisationAvlcompliancecache"] = (
        relationship(
            "OrganisationAvlcompliancecache", uselist=False, back_populates="dataset"
        )
    )
    organisation_datasetsubscription: Mapped[
        List["OrganisationDatasetsubscription"]
    ] = relationship("OrganisationDatasetsubscription", back_populates="dataset")
    organisation_consumerfeedback: Mapped[List["OrganisationConsumerfeedback"]] = (
        relationship("OrganisationConsumerfeedback", back_populates="dataset")
    )


class OrganisationDatasetrevision(Base):
    __tablename__ = "organisation_datasetrevision"
    __table_args__ = (
        CheckConstraint(
            "num_of_bus_stops >= 0",
            name="organisation_datasetrevision_num_of_bus_stops_check",
        ),
        CheckConstraint(
            "num_of_lines >= 0", name="organisation_datasetrevision_num_of_lines_check"
        ),
        CheckConstraint(
            "num_of_operators >= 0",
            name="organisation_datasetrevision_num_of_operators_check",
        ),
        CheckConstraint(
            "num_of_timing_points >= 0",
            name="organisation_datasetrevision_num_of_timing_points_check",
        ),
        ForeignKeyConstraint(
            ["dataset_id"],
            ["organisation_dataset.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_dataset_dataset_id_f0cd70df_fk_organisat",
        ),
        ForeignKeyConstraint(
            ["last_modified_user_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_dataset_last_modified_user_i_cfda7737_fk_users_use",
        ),
        ForeignKeyConstraint(
            ["published_by_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_dataset_published_by_id_4e5c02d1_fk_users_use",
        ),
        PrimaryKeyConstraint("id", name="organisation_datasetrevision_pkey"),
        UniqueConstraint(
            "dataset_id", "created", name="organisation_datasetrevision_unique_revision"
        ),
        UniqueConstraint(
            "name", name="organisation_datasetrevision_name_24f6c4c0_uniq"
        ),
    )

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
    publisher_creation_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True)
    )
    publisher_modified_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True)
    )
    first_expiring_service: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True)
    )
    last_expiring_service: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True)
    )
    first_service_start: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True)
    )
    num_of_bus_stops: Mapped[Optional[int]] = mapped_column(Integer)
    last_modified_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    published_by_id: Mapped[Optional[int]] = mapped_column(Integer)
    published_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    num_of_timing_points: Mapped[Optional[int]] = mapped_column(Integer)

    organisation_dataset: Mapped[Optional["OrganisationDataset"]] = relationship(
        "OrganisationDataset",
        uselist=False,
        foreign_keys="[OrganisationDataset.live_revision_id]",
        back_populates="live_revision",
    )
    dataset: Mapped["OrganisationDataset"] = relationship(
        "OrganisationDataset",
        foreign_keys=[dataset_id],
        back_populates="organisation_datasetrevision",
    )
    last_modified_user: Mapped[Optional["UsersUser"]] = relationship(
        "UsersUser",
        foreign_keys=[last_modified_user_id],
        back_populates="organisation_datasetrevision",
    )
    published_by: Mapped[Optional["UsersUser"]] = relationship(
        "UsersUser",
        foreign_keys=[published_by_id],
        back_populates="organisation_datasetrevision_",
    )
    avl_avlvalidationreport: Mapped[List["AvlAvlvalidationreport"]] = relationship(
        "AvlAvlvalidationreport", back_populates="revision"
    )
    avl_cavlvalidationtaskresult: Mapped[List["AvlCavlvalidationtaskresult"]] = (
        relationship("AvlCavlvalidationtaskresult", back_populates="revision")
    )
    data_quality_dataqualityreport: Mapped[List["DataQualityDataqualityreport"]] = (
        relationship("DataQualityDataqualityreport", back_populates="revision")
    )
    data_quality_postschemaviolation: Mapped[List["DataQualityPostschemaviolation"]] = (
        relationship("DataQualityPostschemaviolation", back_populates="revision")
    )
    data_quality_ptiobservation: Mapped[List["DataQualityPtiobservation"]] = (
        relationship("DataQualityPtiobservation", back_populates="revision")
    )
    data_quality_ptivalidationresult: Mapped["DataQualityPtivalidationresult"] = (
        relationship(
            "DataQualityPtivalidationresult", uselist=False, back_populates="revision"
        )
    )
    data_quality_report: Mapped[List["DataQualityReport"]] = relationship(
        "DataQualityReport", back_populates="revision"
    )
    data_quality_schemaviolation: Mapped[List["DataQualitySchemaviolation"]] = (
        relationship("DataQualitySchemaviolation", back_populates="revision")
    )
    dqs_report: Mapped[List["DqsReport"]] = relationship(
        "DqsReport", back_populates="revision"
    )
    organisation_datasetmetadata: Mapped["OrganisationDatasetmetadata"] = relationship(
        "OrganisationDatasetmetadata", uselist=False, back_populates="revision"
    )
    organisation_txcfileattributes: Mapped[List["OrganisationTxcfileattributes"]] = (
        relationship("OrganisationTxcfileattributes", back_populates="revision")
    )
    pipelines_datasetetlerror: Mapped[List["PipelinesDatasetetlerror"]] = relationship(
        "PipelinesDatasetetlerror", back_populates="revision"
    )
    pipelines_datasetetltaskresult: Mapped[List["PipelinesDatasetetltaskresult"]] = (
        relationship("PipelinesDatasetetltaskresult", back_populates="revision")
    )
    pipelines_fileprocessingresult: Mapped[List["PipelinesFileprocessingresult"]] = (
        relationship("PipelinesFileprocessingresult", back_populates="revision")
    )
    pipelines_remotedatasethealthcheckcount: Mapped[
        "PipelinesRemotedatasethealthcheckcount"
    ] = relationship(
        "PipelinesRemotedatasethealthcheckcount",
        uselist=False,
        back_populates="revision",
    )
    transmodel_servicepattern: Mapped[List["TransmodelServicepattern"]] = relationship(
        "TransmodelServicepattern", back_populates="revision"
    )
    fares_validator_faresvalidation: Mapped[List["FaresValidatorFaresvalidation"]] = (
        relationship("FaresValidatorFaresvalidation", back_populates="revision")
    )
    fares_validator_faresvalidationresult: Mapped[
        "FaresValidatorFaresvalidationresult"
    ] = relationship(
        "FaresValidatorFaresvalidationresult", uselist=False, back_populates="revision"
    )
    organisation_datasetrevision_admin_areas: Mapped[
        List["OrganisationDatasetrevisionAdminAreas"]
    ] = relationship(
        "OrganisationDatasetrevisionAdminAreas", back_populates="datasetrevision"
    )
    pipelines_dataqualitytask: Mapped[List["PipelinesDataqualitytask"]] = relationship(
        "PipelinesDataqualitytask", back_populates="revision"
    )
    transmodel_service: Mapped[List["TransmodelService"]] = relationship(
        "TransmodelService", back_populates="revision"
    )
    organisation_datasetrevision_localities: Mapped[
        List["OrganisationDatasetrevisionLocalities"]
    ] = relationship(
        "OrganisationDatasetrevisionLocalities", back_populates="datasetrevision"
    )
    organisation_consumerfeedback: Mapped[List["OrganisationConsumerfeedback"]] = (
        relationship("OrganisationConsumerfeedback", back_populates="revision")
    )


class OtcInactiveservice(Base):
    __tablename__ = "otc_inactiveservice"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="otc_inactiveservice_pkey"),
        UniqueConstraint(
            "registration_number", name="otc_inactiveservice_registration_number_key"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    registration_number: Mapped[str] = mapped_column(String(20))
    registration_status: Mapped[str] = mapped_column(String(20))
    effective_date: Mapped[Optional[datetime.date]] = mapped_column(Date)


class OtcLicence(Base):
    __tablename__ = "otc_licence"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="otc_licence_pkey"),
        UniqueConstraint("number", name="otc_licence_number_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(9))
    status: Mapped[str] = mapped_column(String(30))
    granted_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    expiry_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    otc_service: Mapped[List["OtcService"]] = relationship(
        "OtcService", back_populates="licence"
    )


class OtcOperator(Base):
    __tablename__ = "otc_operator"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="otc_operator_pkey"),
        UniqueConstraint("operator_id", name="otc_operator_operator_id_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    operator_id: Mapped[int] = mapped_column(Integer)
    operator_name: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(Text)
    discs_in_possession: Mapped[Optional[int]] = mapped_column(Integer)
    authdiscs: Mapped[Optional[int]] = mapped_column(Integer)

    otc_service: Mapped[List["OtcService"]] = relationship(
        "OtcService", back_populates="operator"
    )


class PipelinesBulkdataarchive(Base):
    __tablename__ = "pipelines_bulkdataarchive"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pipelines_bulkdataarchive_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    data: Mapped[str] = mapped_column(String(100))
    dataset_type: Mapped[int] = mapped_column(Integer)
    compliant_archive: Mapped[bool] = mapped_column(Boolean)
    traveline_regions: Mapped[str] = mapped_column(String(4))


class PipelinesChangedataarchive(Base):
    __tablename__ = "pipelines_changedataarchive"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pipelines_changedataarchive_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    published_at: Mapped[datetime.date] = mapped_column(Date)
    data: Mapped[str] = mapped_column(String(100))


class PipelinesPipelineerrorcode(Base):
    __tablename__ = "pipelines_pipelineerrorcode"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pipelines_pipelineerrorcode_pkey"),
        UniqueConstraint("error", name="pipelines_pipelineerrorcode_error_key"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    error: Mapped[str] = mapped_column(String(255))

    pipelines_fileprocessingresult: Mapped[List["PipelinesFileprocessingresult"]] = (
        relationship(
            "PipelinesFileprocessingresult", back_populates="pipeline_error_code"
        )
    )


class PipelinesPipelineprocessingstep(Base):
    __tablename__ = "pipelines_pipelineprocessingstep"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pipelines_pipelineprocessingstep_pkey"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(20))

    pipelines_fileprocessingresult: Mapped[List["PipelinesFileprocessingresult"]] = (
        relationship(
            "PipelinesFileprocessingresult", back_populates="pipeline_processing_step"
        )
    )


class PipelinesSchemadefinition(Base):
    __tablename__ = "pipelines_schemadefinition"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pipelines_schemadefinition_pkey"),
        UniqueConstraint("category", name="pipelines_schemadefinition_category_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    category: Mapped[str] = mapped_column(String(6))
    checksum: Mapped[str] = mapped_column(String(40))
    schema: Mapped[str] = mapped_column(String(100))


class SiteAdminDocumentarchive(Base):
    __tablename__ = "site_admin_documentarchive"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="site_admin_operationalmetricsarchive_pkey"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Sequence("site_admin_operationalmetricsarchive_id_seq"),
        primary_key=True,
    )
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    archive: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(50))


class SiteAdminMetricsarchive(Base):
    __tablename__ = "site_admin_metricsarchive"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="site_admin_metricsarchive_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start: Mapped[datetime.date] = mapped_column(Date)
    end: Mapped[datetime.date] = mapped_column(Date)
    archive: Mapped[str] = mapped_column(String(100))


class SiteAdminOperationalstats(Base):
    __tablename__ = "site_admin_operationalstats"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="site_admin_operationalstats_pkey"),
        UniqueConstraint("date", name="site_admin_operationalstats_date_key"),
    )

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
    __tablename__ = "spatial_ref_sys"
    __table_args__ = (
        CheckConstraint(
            "srid > 0 AND srid <= 998999", name="spatial_ref_sys_srid_check"
        ),
        PrimaryKeyConstraint("srid", name="spatial_ref_sys_pkey"),
    )

    srid: Mapped[int] = mapped_column(Integer, primary_key=True)
    auth_name: Mapped[Optional[str]] = mapped_column(String(256))
    auth_srid: Mapped[Optional[int]] = mapped_column(Integer)
    srtext: Mapped[Optional[str]] = mapped_column(String(2048))
    proj4text: Mapped[Optional[str]] = mapped_column(String(2048))


class TransmodelBankholidays(Base):
    __tablename__ = "transmodel_bankholidays"
    __table_args__ = (PrimaryKeyConstraint("id", name="transmodel_bankholidays_pkey"),)

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    txc_element: Mapped[str] = mapped_column(String(255))
    date: Mapped[datetime.date] = mapped_column(Date)
    title: Mapped[Optional[str]] = mapped_column(String(255))
    notes: Mapped[Optional[str]] = mapped_column(String(255))
    division: Mapped[Optional[str]] = mapped_column(String(255))


class TransmodelServicedorganisations(Base):
    __tablename__ = "transmodel_servicedorganisations"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="transmodel_servicedorganisations_pkey"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    name: Mapped[Optional[str]] = mapped_column(String(255))
    organisation_code: Mapped[Optional[str]] = mapped_column(String(255))

    transmodel_servicedorganisationvehiclejourney: Mapped[
        List["TransmodelServicedorganisationvehiclejourney"]
    ] = relationship(
        "TransmodelServicedorganisationvehiclejourney",
        back_populates="serviced_organisation",
    )


class TransmodelServicelink(Base):
    __tablename__ = "transmodel_servicelink"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="transmodel_servicelink_pkey"),
        UniqueConstraint(
            "from_stop_atco",
            "to_stop_atco",
            name="transmodel_servicelink_from_stop_atco_to_stop_a_06719afb_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    from_stop_atco: Mapped[str] = mapped_column(String(255))
    to_stop_atco: Mapped[str] = mapped_column(String(255))
    from_stop_id: Mapped[Optional[int]] = mapped_column(Integer)
    to_stop_id: Mapped[Optional[int]] = mapped_column(Integer)

    transmodel_servicepattern_service_links: Mapped[
        List["TransmodelServicepatternServiceLinks"]
    ] = relationship(
        "TransmodelServicepatternServiceLinks", back_populates="servicelink"
    )


class TransmodelStopactivity(Base):
    __tablename__ = "transmodel_stopactivity"
    __table_args__ = (PrimaryKeyConstraint("id", name="transmodel_stopactivity_pkey"),)

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(String(255))
    is_pickup: Mapped[bool] = mapped_column(Boolean)
    is_setdown: Mapped[bool] = mapped_column(Boolean)
    is_driverrequest: Mapped[bool] = mapped_column(Boolean)

    transmodel_servicepatternstop: Mapped[List["TransmodelServicepatternstop"]] = (
        relationship("TransmodelServicepatternstop", back_populates="stop_activity")
    )


class TransmodelTracks(Base):
    __tablename__ = "transmodel_tracks"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="transmodel_tracks_pkey"),
        UniqueConstraint(
            "from_atco_code", "to_atco_code", name="unique_from_to_atco_code"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    from_atco_code: Mapped[str] = mapped_column(String(255))
    to_atco_code: Mapped[str] = mapped_column(String(255))
    geometry: Mapped[Optional[Any]] = mapped_column(
        Geometry("LINESTRING", 4326, from_text="ST_GeomFromEWKT", name="geometry")
    )
    distance: Mapped[Optional[int]] = mapped_column(Integer)

    transmodel_tracksvehiclejourney: Mapped[List["TransmodelTracksvehiclejourney"]] = (
        relationship("TransmodelTracksvehiclejourney", back_populates="tracks")
    )


class UiLta(Base):
    __tablename__ = "ui_lta"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="ui_lta_pkey"),
        UniqueConstraint("id", "name", name="ui_lta_id_name_304a2476_uniq"),
        UniqueConstraint("name", name="ui_lta_name_key"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(Text)
    avl_sra: Mapped[Optional[int]] = mapped_column(Integer)
    fares_sra: Mapped[Optional[int]] = mapped_column(Integer)
    overall_sra: Mapped[Optional[int]] = mapped_column(Integer)
    timetable_sra: Mapped[Optional[int]] = mapped_column(Integer)
    total_inscope: Mapped[Optional[int]] = mapped_column(Integer)

    naptan_adminarea: Mapped[List["NaptanAdminarea"]] = relationship(
        "NaptanAdminarea", back_populates="ui_lta"
    )
    otc_localauthority: Mapped[List["OtcLocalauthority"]] = relationship(
        "OtcLocalauthority", back_populates="ui_lta"
    )


class UsersUser(Base):
    __tablename__ = "users_user"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="users_user_pkey"),
        UniqueConstraint("username", name="users_user_username_key"),
    )

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

    organisation_dataset: Mapped[List["OrganisationDataset"]] = relationship(
        "OrganisationDataset", back_populates="contact"
    )
    organisation_datasetrevision: Mapped[List["OrganisationDatasetrevision"]] = (
        relationship(
            "OrganisationDatasetrevision",
            foreign_keys="[OrganisationDatasetrevision.last_modified_user_id]",
            back_populates="last_modified_user",
        )
    )
    organisation_datasetrevision_: Mapped[List["OrganisationDatasetrevision"]] = (
        relationship(
            "OrganisationDatasetrevision",
            foreign_keys="[OrganisationDatasetrevision.published_by_id]",
            back_populates="published_by",
        )
    )
    account_emailaddress: Mapped[List["AccountEmailaddress"]] = relationship(
        "AccountEmailaddress", back_populates="user"
    )
    authtoken_token: Mapped["AuthtokenToken"] = relationship(
        "AuthtokenToken", uselist=False, back_populates="user"
    )
    django_admin_log: Mapped[List["DjangoAdminLog"]] = relationship(
        "DjangoAdminLog", back_populates="user"
    )
    invitations_invitation: Mapped[List["InvitationsInvitation"]] = relationship(
        "InvitationsInvitation", back_populates="inviter"
    )
    organisation_datasetsubscription: Mapped[
        List["OrganisationDatasetsubscription"]
    ] = relationship("OrganisationDatasetsubscription", back_populates="user")
    organisation_organisation: Mapped[Optional["OrganisationOrganisation"]] = (
        relationship(
            "OrganisationOrganisation", uselist=False, back_populates="key_contact"
        )
    )
    restrict_sessions_loggedinuser: Mapped["RestrictSessionsLoggedinuser"] = (
        relationship(
            "RestrictSessionsLoggedinuser", uselist=False, back_populates="user"
        )
    )
    site_admin_apirequest: Mapped[List["SiteAdminApirequest"]] = relationship(
        "SiteAdminApirequest", back_populates="requestor"
    )
    site_admin_resourcerequestcounter: Mapped[
        List["SiteAdminResourcerequestcounter"]
    ] = relationship("SiteAdminResourcerequestcounter", back_populates="requestor")
    users_user_groups: Mapped[List["UsersUserGroups"]] = relationship(
        "UsersUserGroups", back_populates="user"
    )
    waffle_flag_users: Mapped[List["WaffleFlagUsers"]] = relationship(
        "WaffleFlagUsers", back_populates="user"
    )
    users_user_organisations: Mapped[List["UsersUserOrganisations"]] = relationship(
        "UsersUserOrganisations", back_populates="user"
    )
    users_user_user_permissions: Mapped[List["UsersUserUserPermissions"]] = (
        relationship("UsersUserUserPermissions", back_populates="user")
    )
    organisation_servicecodeexemption: Mapped[
        List["OrganisationServicecodeexemption"]
    ] = relationship("OrganisationServicecodeexemption", back_populates="exempted_by")
    users_agentuserinvite: Mapped[List["UsersAgentuserinvite"]] = relationship(
        "UsersAgentuserinvite",
        foreign_keys="[UsersAgentuserinvite.agent_id]",
        back_populates="agent",
    )
    users_agentuserinvite_: Mapped[List["UsersAgentuserinvite"]] = relationship(
        "UsersAgentuserinvite",
        foreign_keys="[UsersAgentuserinvite.inviter_id]",
        back_populates="inviter",
    )
    organisation_consumerfeedback: Mapped[List["OrganisationConsumerfeedback"]] = (
        relationship("OrganisationConsumerfeedback", back_populates="consumer")
    )


class WaffleFlag(Base):
    __tablename__ = "waffle_flag"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="waffle_flag_pkey"),
        UniqueConstraint("name", name="waffle_flag_name_key"),
    )

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

    waffle_flag_groups: Mapped[List["WaffleFlagGroups"]] = relationship(
        "WaffleFlagGroups", back_populates="flag"
    )
    waffle_flag_users: Mapped[List["WaffleFlagUsers"]] = relationship(
        "WaffleFlagUsers", back_populates="flag"
    )


class WaffleSample(Base):
    __tablename__ = "waffle_sample"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="waffle_sample_pkey"),
        UniqueConstraint("name", name="waffle_sample_name_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    percent: Mapped[decimal.Decimal] = mapped_column(Numeric(4, 1))
    note: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))


class WaffleSwitch(Base):
    __tablename__ = "waffle_switch"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="waffle_switch_pkey"),
        UniqueConstraint("name", name="waffle_switch_name_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    active: Mapped[bool] = mapped_column(Boolean)
    note: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))


class AccountEmailaddress(Base):
    __tablename__ = "account_emailaddress"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="account_emailaddress_user_id_2c513194_fk_users_user_id",
        ),
        PrimaryKeyConstraint("id", name="account_emailaddress_pkey"),
        UniqueConstraint(
            "user_id", "email", name="account_emailaddress_user_id_email_987c8728_uniq"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(254))
    verified: Mapped[bool] = mapped_column(Boolean)
    primary: Mapped[bool] = mapped_column(Boolean)
    user_id: Mapped[int] = mapped_column(Integer)

    user: Mapped["UsersUser"] = relationship(
        "UsersUser", back_populates="account_emailaddress"
    )
    account_emailconfirmation: Mapped[List["AccountEmailconfirmation"]] = relationship(
        "AccountEmailconfirmation", back_populates="email_address"
    )


class AuthPermission(Base):
    __tablename__ = "auth_permission"
    __table_args__ = (
        ForeignKeyConstraint(
            ["content_type_id"],
            ["django_content_type.id"],
            deferrable=True,
            initially="DEFERRED",
            name="auth_permission_content_type_id_2f476e4b_fk_django_co",
        ),
        PrimaryKeyConstraint("id", name="auth_permission_pkey"),
        UniqueConstraint(
            "content_type_id",
            "codename",
            name="auth_permission_content_type_id_codename_01ab375a_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    content_type_id: Mapped[int] = mapped_column(Integer)
    codename: Mapped[str] = mapped_column(String(100))

    content_type: Mapped["DjangoContentType"] = relationship(
        "DjangoContentType", back_populates="auth_permission"
    )
    auth_group_permissions: Mapped[List["AuthGroupPermissions"]] = relationship(
        "AuthGroupPermissions", back_populates="permission"
    )
    users_user_user_permissions: Mapped[List["UsersUserUserPermissions"]] = (
        relationship("UsersUserUserPermissions", back_populates="permission")
    )


class AuthtokenToken(Base):
    __tablename__ = "authtoken_token"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="authtoken_token_user_id_35299eff_fk_users_user_id",
        ),
        PrimaryKeyConstraint("key", name="authtoken_token_pkey"),
        UniqueConstraint("user_id", name="authtoken_token_user_id_key"),
    )

    key: Mapped[str] = mapped_column(String(40), primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    user_id: Mapped[int] = mapped_column(Integer)

    user: Mapped["UsersUser"] = relationship(
        "UsersUser", back_populates="authtoken_token"
    )


class AvlAvlvalidationreport(Base):
    __tablename__ = "avl_avlvalidationreport"
    __table_args__ = (
        CheckConstraint(
            "critical_count >= 0",
            name="avl_avlvalidationreport_critical_count_d4af7489_check",
        ),
        CheckConstraint(
            "non_critical_count >= 0",
            name="avl_avlvalidationreport_non_critical_count_9b18ca51_check",
        ),
        CheckConstraint(
            "vehicle_activity_count >= 0",
            name="avl_avlvalidationreport_vehicle_activity_count_check",
        ),
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="avl_avlvalidationrep_revision_id_4a705df5_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="avl_avlvalidationreport_pkey"),
        UniqueConstraint(
            "revision_id",
            "created",
            name="avl_avlvalidationreport_revision_id_created_9ed39c62_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    critical_count: Mapped[int] = mapped_column(Integer)
    non_critical_count: Mapped[int] = mapped_column(Integer)
    created: Mapped[datetime.date] = mapped_column(Date)
    revision_id: Mapped[int] = mapped_column(Integer)
    critical_score: Mapped[float] = mapped_column(Double(53))
    non_critical_score: Mapped[float] = mapped_column(Double(53))
    vehicle_activity_count: Mapped[int] = mapped_column(Integer)
    file: Mapped[Optional[str]] = mapped_column(String(100))

    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision", back_populates="avl_avlvalidationreport"
    )


class AvlCavlvalidationtaskresult(Base):
    __tablename__ = "avl_cavlvalidationtaskresult"
    __table_args__ = (
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="avl_cavlvalidationta_revision_id_39f298bd_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="avl_cavlvalidationtaskresult_pkey"),
        UniqueConstraint("task_id", name="avl_cavlvalidationtaskresult_task_id_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    task_id: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50))
    revision_id: Mapped[int] = mapped_column(Integer)
    result: Mapped[str] = mapped_column(String(50))
    completed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision", back_populates="avl_cavlvalidationtaskresult"
    )


class AvlPostpublishingcheckreport(Base):
    __tablename__ = "avl_postpublishingcheckreport"
    __table_args__ = (
        CheckConstraint(
            "vehicle_activities_analysed >= 0",
            name="avl_postpublishingcheck_vehicle_activities_anal_5d2f8bb2_check",
        ),
        CheckConstraint(
            "vehicle_activities_completely_matching >= 0",
            name="avl_postpublishingcheck_vehicle_activities_comp_b4bb7756_check",
        ),
        ForeignKeyConstraint(
            ["dataset_id"],
            ["organisation_dataset.id"],
            deferrable=True,
            initially="DEFERRED",
            name="avl_postpublishingch_dataset_id_63c55892_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="avl_postpublishingcheckreport_pkey"),
        UniqueConstraint("dataset_id", "granularity", "created", name="unique_report"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.date] = mapped_column(Date)
    granularity: Mapped[str] = mapped_column(String(6))
    file: Mapped[str] = mapped_column(String(100))
    dataset_id: Mapped[int] = mapped_column(Integer)
    vehicle_activities_analysed: Mapped[Optional[int]] = mapped_column(Integer)
    vehicle_activities_completely_matching: Mapped[Optional[int]] = mapped_column(
        Integer
    )

    dataset: Mapped["OrganisationDataset"] = relationship(
        "OrganisationDataset", back_populates="avl_postpublishingcheckreport"
    )


class DataQualityDataqualityreport(Base):
    __tablename__ = "data_quality_dataqualityreport"
    __table_args__ = (
        CheckConstraint(
            "score >= 0.0::double precision AND score <= 1.0::double precision",
            name="dq_score_must_be_between_0_and_1",
        ),
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_dataqua_revision_id_e5f9faef_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="data_quality_dataqualityreport_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    file: Mapped[str] = mapped_column(String(100))
    revision_id: Mapped[int] = mapped_column(Integer)
    score: Mapped[float] = mapped_column(Double(53))

    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision", back_populates="data_quality_dataqualityreport"
    )
    data_quality_dataqualityreportsummary: Mapped[
        "DataQualityDataqualityreportsummary"
    ] = relationship(
        "DataQualityDataqualityreportsummary", uselist=False, back_populates="report"
    )
    data_quality_fastlinkwarning: Mapped[List["DataQualityFastlinkwarning"]] = (
        relationship("DataQualityFastlinkwarning", back_populates="report")
    )
    data_quality_fasttimingwarning: Mapped[List["DataQualityFasttimingwarning"]] = (
        relationship("DataQualityFasttimingwarning", back_populates="report")
    )
    data_quality_incorrectnocwarning: Mapped[List["DataQualityIncorrectnocwarning"]] = (
        relationship("DataQualityIncorrectnocwarning", back_populates="report")
    )
    data_quality_journeyconflictwarning: Mapped[
        List["DataQualityJourneyconflictwarning"]
    ] = relationship("DataQualityJourneyconflictwarning", back_populates="report")
    data_quality_journeydaterangebackwardswarning: Mapped[
        List["DataQualityJourneydaterangebackwardswarning"]
    ] = relationship(
        "DataQualityJourneydaterangebackwardswarning", back_populates="report"
    )
    data_quality_journeyduplicatewarning: Mapped[
        List["DataQualityJourneyduplicatewarning"]
    ] = relationship("DataQualityJourneyduplicatewarning", back_populates="report")
    data_quality_journeystopinappropriatewarning: Mapped[
        List["DataQualityJourneystopinappropriatewarning"]
    ] = relationship(
        "DataQualityJourneystopinappropriatewarning", back_populates="report"
    )
    data_quality_journeywithoutheadsignwarning: Mapped[
        List["DataQualityJourneywithoutheadsignwarning"]
    ] = relationship(
        "DataQualityJourneywithoutheadsignwarning", back_populates="report"
    )
    data_quality_lineexpiredwarning: Mapped[List["DataQualityLineexpiredwarning"]] = (
        relationship("DataQualityLineexpiredwarning", back_populates="report")
    )
    data_quality_linemissingblockidwarning: Mapped[
        List["DataQualityLinemissingblockidwarning"]
    ] = relationship("DataQualityLinemissingblockidwarning", back_populates="report")
    data_quality_service_reports: Mapped[List["DataQualityServiceReports"]] = (
        relationship("DataQualityServiceReports", back_populates="dataqualityreport")
    )
    data_quality_servicelinkmissingstopwarning: Mapped[
        List["DataQualityServicelinkmissingstopwarning"]
    ] = relationship(
        "DataQualityServicelinkmissingstopwarning", back_populates="report"
    )
    data_quality_slowlinkwarning: Mapped[List["DataQualitySlowlinkwarning"]] = (
        relationship("DataQualitySlowlinkwarning", back_populates="report")
    )
    data_quality_slowtimingwarning: Mapped[List["DataQualitySlowtimingwarning"]] = (
        relationship("DataQualitySlowtimingwarning", back_populates="report")
    )
    data_quality_stopincorrecttypewarning: Mapped[
        List["DataQualityStopincorrecttypewarning"]
    ] = relationship("DataQualityStopincorrecttypewarning", back_populates="report")
    data_quality_stopmissingnaptanwarning: Mapped[
        List["DataQualityStopmissingnaptanwarning"]
    ] = relationship("DataQualityStopmissingnaptanwarning", back_populates="report")
    data_quality_timingbackwardswarning: Mapped[
        List["DataQualityTimingbackwardswarning"]
    ] = relationship("DataQualityTimingbackwardswarning", back_populates="report")
    data_quality_timingdropoffwarning: Mapped[
        List["DataQualityTimingdropoffwarning"]
    ] = relationship("DataQualityTimingdropoffwarning", back_populates="report")
    data_quality_timingfirstwarning: Mapped[List["DataQualityTimingfirstwarning"]] = (
        relationship("DataQualityTimingfirstwarning", back_populates="report")
    )
    data_quality_timinglastwarning: Mapped[List["DataQualityTiminglastwarning"]] = (
        relationship("DataQualityTiminglastwarning", back_populates="report")
    )
    data_quality_timingmissingpointwarning: Mapped[
        List["DataQualityTimingmissingpointwarning"]
    ] = relationship("DataQualityTimingmissingpointwarning", back_populates="report")
    data_quality_timingmultiplewarning: Mapped[
        List["DataQualityTimingmultiplewarning"]
    ] = relationship("DataQualityTimingmultiplewarning", back_populates="report")
    data_quality_timingpickupwarning: Mapped[List["DataQualityTimingpickupwarning"]] = (
        relationship("DataQualityTimingpickupwarning", back_populates="report")
    )
    pipelines_dataqualitytask: Mapped[Optional["PipelinesDataqualitytask"]] = (
        relationship("PipelinesDataqualitytask", uselist=False, back_populates="report")
    )


class DataQualityPostschemaviolation(Base):
    __tablename__ = "data_quality_postschemaviolation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_postsch_revision_id_d236c059_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="data_quality_postschemaviolation_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(256))
    details: Mapped[str] = mapped_column(String(1024))
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    revision_id: Mapped[int] = mapped_column(Integer)
    additional_details: Mapped[Optional[dict]] = mapped_column(JSONB)

    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision", back_populates="data_quality_postschemaviolation"
    )


class DataQualityPtiobservation(Base):
    __tablename__ = "data_quality_ptiobservation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_ptiobse_revision_id_3206212f_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="data_quality_ptiobservation_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(256))
    line: Mapped[int] = mapped_column(Integer)
    details: Mapped[str] = mapped_column(String(1024))
    element: Mapped[str] = mapped_column(String(256))
    category: Mapped[str] = mapped_column(String(1024))
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    revision_id: Mapped[int] = mapped_column(Integer)
    reference: Mapped[str] = mapped_column(String(64))

    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision", back_populates="data_quality_ptiobservation"
    )


class DataQualityPtivalidationresult(Base):
    __tablename__ = "data_quality_ptivalidationresult"
    __table_args__ = (
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_ptivali_revision_id_a90de4ea_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="data_quality_ptivalidationresult_pkey"),
        UniqueConstraint(
            "revision_id", name="data_quality_ptivalidationresult_revision_id_key"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    count: Mapped[int] = mapped_column(Integer)
    report: Mapped[str] = mapped_column(String(100))
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    revision_id: Mapped[int] = mapped_column(Integer)

    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision", back_populates="data_quality_ptivalidationresult"
    )


class DataQualityReport(Base):
    __tablename__ = "data_quality_report"
    __table_args__ = (
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_report_revision_id_11478559_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="data_quality_report_pkey"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    file_name: Mapped[str] = mapped_column(String(255))
    revision_id: Mapped[int] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(String(64))

    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision", back_populates="data_quality_report"
    )
    data_quality_taskresults: Mapped[List["DataQualityTaskresults"]] = relationship(
        "DataQualityTaskresults", back_populates="dataquality_report"
    )


class DataQualitySchemaviolation(Base):
    __tablename__ = "data_quality_schemaviolation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_schemav_revision_id_09049f6e_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="data_quality_schemaviolation_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(256))
    line: Mapped[int] = mapped_column(Integer)
    details: Mapped[str] = mapped_column(String(1024))
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    revision_id: Mapped[int] = mapped_column(Integer)

    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision", back_populates="data_quality_schemaviolation"
    )


class DataQualityTimingpatternstop(Base):
    __tablename__ = "data_quality_timingpatternstop"
    __table_args__ = (
        ForeignKeyConstraint(
            ["service_pattern_stop_id"],
            ["data_quality_servicepatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingp_service_pattern_stop_0029574c_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timing_pattern_id"],
            ["data_quality_timingpattern.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingp_timing_pattern_id_4ad1bb50_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_timingpatternstop_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    arrival: Mapped[datetime.timedelta] = mapped_column(INTERVAL)
    departure: Mapped[datetime.timedelta] = mapped_column(INTERVAL)
    pickup_allowed: Mapped[bool] = mapped_column(Boolean)
    setdown_allowed: Mapped[bool] = mapped_column(Boolean)
    timing_point: Mapped[bool] = mapped_column(Boolean)
    service_pattern_stop_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    service_pattern_stop: Mapped["DataQualityServicepatternstop"] = relationship(
        "DataQualityServicepatternstop", back_populates="data_quality_timingpatternstop"
    )
    timing_pattern: Mapped["DataQualityTimingpattern"] = relationship(
        "DataQualityTimingpattern", back_populates="data_quality_timingpatternstop"
    )
    data_quality_timingbackwardswarning: Mapped[
        List["DataQualityTimingbackwardswarning"]
    ] = relationship(
        "DataQualityTimingbackwardswarning",
        foreign_keys="[DataQualityTimingbackwardswarning.from_stop_id]",
        back_populates="from_stop",
    )
    data_quality_timingbackwardswarning_: Mapped[
        List["DataQualityTimingbackwardswarning"]
    ] = relationship(
        "DataQualityTimingbackwardswarning",
        foreign_keys="[DataQualityTimingbackwardswarning.to_stop_id]",
        back_populates="to_stop",
    )
    data_quality_fastlinkwarning_timings: Mapped[
        List["DataQualityFastlinkwarningTimings"]
    ] = relationship(
        "DataQualityFastlinkwarningTimings", back_populates="timingpatternstop"
    )
    data_quality_fasttimingwarning_timings: Mapped[
        List["DataQualityFasttimingwarningTimings"]
    ] = relationship(
        "DataQualityFasttimingwarningTimings", back_populates="timingpatternstop"
    )
    data_quality_slowlinkwarning_timings: Mapped[
        List["DataQualitySlowlinkwarningTimings"]
    ] = relationship(
        "DataQualitySlowlinkwarningTimings", back_populates="timingpatternstop"
    )
    data_quality_slowtimingwarning_timings: Mapped[
        List["DataQualitySlowtimingwarningTimings"]
    ] = relationship(
        "DataQualitySlowtimingwarningTimings", back_populates="timingpatternstop"
    )
    data_quality_timingbackwardswarning_timings: Mapped[
        List["DataQualityTimingbackwardswarningTimings"]
    ] = relationship(
        "DataQualityTimingbackwardswarningTimings", back_populates="timingpatternstop"
    )
    data_quality_timingdropoffwarning_timings: Mapped[
        List["DataQualityTimingdropoffwarningTimings"]
    ] = relationship(
        "DataQualityTimingdropoffwarningTimings", back_populates="timingpatternstop"
    )
    data_quality_timingfirstwarning_timings: Mapped[
        List["DataQualityTimingfirstwarningTimings"]
    ] = relationship(
        "DataQualityTimingfirstwarningTimings", back_populates="timingpatternstop"
    )
    data_quality_timinglastwarning_timings: Mapped[
        List["DataQualityTiminglastwarningTimings"]
    ] = relationship(
        "DataQualityTiminglastwarningTimings", back_populates="timingpatternstop"
    )
    data_quality_timingmissingpointwarning_timings: Mapped[
        List["DataQualityTimingmissingpointwarningTimings"]
    ] = relationship(
        "DataQualityTimingmissingpointwarningTimings",
        back_populates="timingpatternstop",
    )
    data_quality_timingmultiplewarning_timings: Mapped[
        List["DataQualityTimingmultiplewarningTimings"]
    ] = relationship(
        "DataQualityTimingmultiplewarningTimings", back_populates="timingpatternstop"
    )
    data_quality_timingpickupwarning_timings: Mapped[
        List["DataQualityTimingpickupwarningTimings"]
    ] = relationship(
        "DataQualityTimingpickupwarningTimings", back_populates="timingpatternstop"
    )


class DataQualityVehiclejourney(Base):
    __tablename__ = "data_quality_vehiclejourney"
    __table_args__ = (
        ForeignKeyConstraint(
            ["timing_pattern_id"],
            ["data_quality_timingpattern.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_vehicle_timing_pattern_id_bf248874_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_vehiclejourney_pkey"),
        UniqueConstraint("ito_id", name="data_quality_vehiclejourney_ito_id_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[datetime.time] = mapped_column(Time)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)
    ito_id: Mapped[str] = mapped_column(Text)
    dates: Mapped[list] = mapped_column(ARRAY(Date()))

    timing_pattern: Mapped["DataQualityTimingpattern"] = relationship(
        "DataQualityTimingpattern", back_populates="data_quality_vehiclejourney"
    )
    data_quality_journeyconflictwarning: Mapped[
        List["DataQualityJourneyconflictwarning"]
    ] = relationship(
        "DataQualityJourneyconflictwarning",
        foreign_keys="[DataQualityJourneyconflictwarning.conflict_id]",
        back_populates="conflict",
    )
    data_quality_journeyconflictwarning_: Mapped[
        List["DataQualityJourneyconflictwarning"]
    ] = relationship(
        "DataQualityJourneyconflictwarning",
        foreign_keys="[DataQualityJourneyconflictwarning.vehicle_journey_id]",
        back_populates="vehicle_journey",
    )
    data_quality_journeydaterangebackwardswarning: Mapped[
        List["DataQualityJourneydaterangebackwardswarning"]
    ] = relationship(
        "DataQualityJourneydaterangebackwardswarning", back_populates="vehicle_journey"
    )
    data_quality_journeyduplicatewarning: Mapped[
        List["DataQualityJourneyduplicatewarning"]
    ] = relationship(
        "DataQualityJourneyduplicatewarning",
        foreign_keys="[DataQualityJourneyduplicatewarning.duplicate_id]",
        back_populates="duplicate",
    )
    data_quality_journeyduplicatewarning_: Mapped[
        List["DataQualityJourneyduplicatewarning"]
    ] = relationship(
        "DataQualityJourneyduplicatewarning",
        foreign_keys="[DataQualityJourneyduplicatewarning.vehicle_journey_id]",
        back_populates="vehicle_journey",
    )
    data_quality_journeywithoutheadsignwarning: Mapped[
        List["DataQualityJourneywithoutheadsignwarning"]
    ] = relationship(
        "DataQualityJourneywithoutheadsignwarning", back_populates="vehicle_journey"
    )
    data_quality_journeystopinappropriatewarning_vehicle_journeys: Mapped[
        List["DataQualityJourneystopinappropriatewarningVehicleJourneys"]
    ] = relationship(
        "DataQualityJourneystopinappropriatewarningVehicleJourneys",
        back_populates="vehiclejourney",
    )
    data_quality_lineexpiredwarning_vehicle_journeys: Mapped[
        List["DataQualityLineexpiredwarningVehicleJourneys"]
    ] = relationship(
        "DataQualityLineexpiredwarningVehicleJourneys", back_populates="vehiclejourney"
    )
    data_quality_linemissingblockidwarning_vehicle_journeys: Mapped[
        List["DataQualityLinemissingblockidwarningVehicleJourneys"]
    ] = relationship(
        "DataQualityLinemissingblockidwarningVehicleJourneys",
        back_populates="vehiclejourney",
    )


class DjangoAdminLog(Base):
    __tablename__ = "django_admin_log"
    __table_args__ = (
        CheckConstraint("action_flag >= 0", name="django_admin_log_action_flag_check"),
        ForeignKeyConstraint(
            ["content_type_id"],
            ["django_content_type.id"],
            deferrable=True,
            initially="DEFERRED",
            name="django_admin_log_content_type_id_c4bce8eb_fk_django_co",
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="django_admin_log_user_id_c564eba6_fk_users_user_id",
        ),
        PrimaryKeyConstraint("id", name="django_admin_log_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action_time: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    object_repr: Mapped[str] = mapped_column(String(200))
    action_flag: Mapped[int] = mapped_column(SmallInteger)
    change_message: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(Integer)
    object_id: Mapped[Optional[str]] = mapped_column(Text)
    content_type_id: Mapped[Optional[int]] = mapped_column(Integer)

    content_type: Mapped[Optional["DjangoContentType"]] = relationship(
        "DjangoContentType", back_populates="django_admin_log"
    )
    user: Mapped["UsersUser"] = relationship(
        "UsersUser", back_populates="django_admin_log"
    )


class DjangoCeleryBeatPeriodictask(Base):
    __tablename__ = "django_celery_beat_periodictask"
    __table_args__ = (
        CheckConstraint(
            "expire_seconds >= 0",
            name="django_celery_beat_periodictask_expire_seconds_check",
        ),
        CheckConstraint(
            "priority >= 0", name="django_celery_beat_periodictask_priority_check"
        ),
        CheckConstraint(
            "total_run_count >= 0",
            name="django_celery_beat_periodictask_total_run_count_check",
        ),
        ForeignKeyConstraint(
            ["clocked_id"],
            ["django_celery_beat_clockedschedule.id"],
            deferrable=True,
            initially="DEFERRED",
            name="django_celery_beat_p_clocked_id_47a69f82_fk_django_ce",
        ),
        ForeignKeyConstraint(
            ["crontab_id"],
            ["django_celery_beat_crontabschedule.id"],
            deferrable=True,
            initially="DEFERRED",
            name="django_celery_beat_p_crontab_id_d3cba168_fk_django_ce",
        ),
        ForeignKeyConstraint(
            ["interval_id"],
            ["django_celery_beat_intervalschedule.id"],
            deferrable=True,
            initially="DEFERRED",
            name="django_celery_beat_p_interval_id_a8ca27da_fk_django_ce",
        ),
        ForeignKeyConstraint(
            ["solar_id"],
            ["django_celery_beat_solarschedule.id"],
            deferrable=True,
            initially="DEFERRED",
            name="django_celery_beat_p_solar_id_a87ce72c_fk_django_ce",
        ),
        PrimaryKeyConstraint("id", name="django_celery_beat_periodictask_pkey"),
        UniqueConstraint("name", name="django_celery_beat_periodictask_name_key"),
    )

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

    clocked: Mapped[Optional["DjangoCeleryBeatClockedschedule"]] = relationship(
        "DjangoCeleryBeatClockedschedule",
        back_populates="django_celery_beat_periodictask",
    )
    crontab: Mapped[Optional["DjangoCeleryBeatCrontabschedule"]] = relationship(
        "DjangoCeleryBeatCrontabschedule",
        back_populates="django_celery_beat_periodictask",
    )
    interval: Mapped[Optional["DjangoCeleryBeatIntervalschedule"]] = relationship(
        "DjangoCeleryBeatIntervalschedule",
        back_populates="django_celery_beat_periodictask",
    )
    solar: Mapped[Optional["DjangoCeleryBeatSolarschedule"]] = relationship(
        "DjangoCeleryBeatSolarschedule",
        back_populates="django_celery_beat_periodictask",
    )


class DqsReport(Base):
    __tablename__ = "dqs_report"
    __table_args__ = (
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="dqs_report_revision_id_6eda8a8d_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="dqs_report_pkey"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    file_name: Mapped[str] = mapped_column(String(255))
    revision_id: Mapped[int] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(String(64))

    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision", back_populates="dqs_report"
    )
    dqs_taskresults: Mapped[List["DqsTaskresults"]] = relationship(
        "DqsTaskresults", back_populates="dataquality_report"
    )


class InvitationsInvitation(Base):
    __tablename__ = "invitations_invitation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["inviter_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="invitations_invitation_inviter_id_83070e1a_fk_users_user_id",
        ),
        PrimaryKeyConstraint("id", name="invitations_invitation_pkey"),
        UniqueConstraint("email", name="invitations_invitation_email_key"),
        UniqueConstraint("key", name="invitations_invitation_key_key"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(String(254))
    accepted: Mapped[bool] = mapped_column(Boolean)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    key: Mapped[str] = mapped_column(String(64))
    sent: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    inviter_id: Mapped[Optional[int]] = mapped_column(Integer)

    inviter: Mapped[Optional["UsersUser"]] = relationship(
        "UsersUser", back_populates="invitations_invitation"
    )


class NaptanAdminarea(Base):
    __tablename__ = "naptan_adminarea"
    __table_args__ = (
        ForeignKeyConstraint(
            ["ui_lta_id"],
            ["ui_lta.id"],
            deferrable=True,
            initially="DEFERRED",
            name="naptan_adminarea_ui_lta_id_c37d8a17_fk_ui_lta_id",
        ),
        PrimaryKeyConstraint("id", name="naptan_adminarea_pkey"),
        UniqueConstraint("atco_code", name="naptan_adminarea_atco_code_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    traveline_region_id: Mapped[str] = mapped_column(String(255))
    atco_code: Mapped[str] = mapped_column(String(255))
    ui_lta_id: Mapped[Optional[int]] = mapped_column(Integer)

    ui_lta: Mapped[Optional["UiLta"]] = relationship(
        "UiLta", back_populates="naptan_adminarea"
    )
    naptan_locality: Mapped[List["NaptanLocality"]] = relationship(
        "NaptanLocality", back_populates="admin_area"
    )
    organisation_datasetrevision_admin_areas: Mapped[
        List["OrganisationDatasetrevisionAdminAreas"]
    ] = relationship(
        "OrganisationDatasetrevisionAdminAreas", back_populates="adminarea"
    )
    organisation_organisation_admin_areas: Mapped[
        List["OrganisationOrganisationAdminAreas"]
    ] = relationship("OrganisationOrganisationAdminAreas", back_populates="adminarea")
    transmodel_servicepattern_admin_areas: Mapped[
        List["TransmodelServicepatternAdminAreas"]
    ] = relationship("TransmodelServicepatternAdminAreas", back_populates="adminarea")
    naptan_stoppoint: Mapped[List["NaptanStoppoint"]] = relationship(
        "NaptanStoppoint", back_populates="admin_area"
    )


class OrganisationAvlcompliancecache(Base):
    __tablename__ = "organisation_avlcompliancecache"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataset_id"],
            ["organisation_dataset.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_avlcomp_dataset_id_80a23bf9_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="organisation_avlcompliancecache_pkey"),
        UniqueConstraint(
            "dataset_id", name="organisation_avlcompliancecache_dataset_id_key"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String(50))
    dataset_id: Mapped[int] = mapped_column(Integer)

    dataset: Mapped["OrganisationDataset"] = relationship(
        "OrganisationDataset", back_populates="organisation_avlcompliancecache"
    )


class OrganisationDatasetmetadata(Base):
    __tablename__ = "organisation_datasetmetadata"
    __table_args__ = (
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_dataset_revision_id_ba64cf5c_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="organisation_datasetmetadata_pkey"),
        UniqueConstraint(
            "revision_id", name="organisation_datasetmetadata_revision_id_key"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    schema_version: Mapped[str] = mapped_column(String(8))
    revision_id: Mapped[int] = mapped_column(Integer)

    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision", back_populates="organisation_datasetmetadata"
    )


class OrganisationDatasetsubscription(Base):
    __tablename__ = "organisation_datasetsubscription"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataset_id"],
            ["organisation_dataset.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_dataset_dataset_id_21ca02dc_fk_organisat",
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_dataset_user_id_dfae43a9_fk_users_use",
        ),
        PrimaryKeyConstraint("id", name="organisation_datasetsubscription_pkey"),
        UniqueConstraint(
            "dataset_id",
            "user_id",
            name="organisation_datasetsubs_dataset_id_user_id_9b39e676_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    dataset_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)

    dataset: Mapped["OrganisationDataset"] = relationship(
        "OrganisationDataset", back_populates="organisation_datasetsubscription"
    )
    user: Mapped["UsersUser"] = relationship(
        "UsersUser", back_populates="organisation_datasetsubscription"
    )


class OrganisationOrganisation(Base):
    __tablename__ = "organisation_organisation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["key_contact_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_organis_key_contact_id_df58d4ce_fk_users_use",
        ),
        PrimaryKeyConstraint("id", name="organisation_organisation_pkey"),
        UniqueConstraint(
            "key_contact_id", name="organisation_organisation_key_contact_id_key"
        ),
        UniqueConstraint("name", name="organisation_organisation_name_6b81abae_uniq"),
    )

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

    organisation_dataset: Mapped[List["OrganisationDataset"]] = relationship(
        "OrganisationDataset", back_populates="organisation"
    )
    key_contact: Mapped[Optional["UsersUser"]] = relationship(
        "UsersUser", back_populates="organisation_organisation"
    )
    fares_validator_faresvalidation: Mapped[List["FaresValidatorFaresvalidation"]] = (
        relationship("FaresValidatorFaresvalidation", back_populates="organisation")
    )
    fares_validator_faresvalidationresult: Mapped[
        List["FaresValidatorFaresvalidationresult"]
    ] = relationship(
        "FaresValidatorFaresvalidationresult", back_populates="organisation"
    )
    organisation_consumerstats: Mapped["OrganisationConsumerstats"] = relationship(
        "OrganisationConsumerstats", uselist=False, back_populates="organisation"
    )
    organisation_licence: Mapped[List["OrganisationLicence"]] = relationship(
        "OrganisationLicence", back_populates="organisation"
    )
    organisation_operatorcode: Mapped[List["OrganisationOperatorcode"]] = relationship(
        "OrganisationOperatorcode", back_populates="organisation"
    )
    organisation_organisation_admin_areas: Mapped[
        List["OrganisationOrganisationAdminAreas"]
    ] = relationship(
        "OrganisationOrganisationAdminAreas", back_populates="organisation"
    )
    users_invitation: Mapped[List["UsersInvitation"]] = relationship(
        "UsersInvitation", back_populates="organisation"
    )
    users_user_organisations: Mapped[List["UsersUserOrganisations"]] = relationship(
        "UsersUserOrganisations", back_populates="organisation"
    )
    users_agentuserinvite: Mapped[List["UsersAgentuserinvite"]] = relationship(
        "UsersAgentuserinvite", back_populates="organisation"
    )
    organisation_consumerfeedback: Mapped[List["OrganisationConsumerfeedback"]] = (
        relationship("OrganisationConsumerfeedback", back_populates="organisation")
    )


class OrganisationTxcfileattributes(Base):
    __tablename__ = "organisation_txcfileattributes"
    __table_args__ = (
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_txcfile_revision_id_ddb2f841_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="organisation_txcfileattributes_pkey"),
    )

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

    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision", back_populates="organisation_txcfileattributes"
    )
    data_quality_taskresults: Mapped[List["DataQualityTaskresults"]] = relationship(
        "DataQualityTaskresults", back_populates="transmodel_txcfileattributes"
    )
    dqs_taskresults: Mapped[List["DqsTaskresults"]] = relationship(
        "DqsTaskresults", back_populates="transmodel_txcfileattributes"
    )
    transmodel_service: Mapped[List["TransmodelService"]] = relationship(
        "TransmodelService", back_populates="txcfileattributes"
    )


class OtcLocalauthority(Base):
    __tablename__ = "otc_localauthority"
    __table_args__ = (
        ForeignKeyConstraint(
            ["ui_lta_id"],
            ["ui_lta.id"],
            deferrable=True,
            initially="DEFERRED",
            name="otc_localauthority_ui_lta_id_f47b3d37_fk_ui_lta_id",
        ),
        PrimaryKeyConstraint("id", name="otc_localauthority_pkey"),
        UniqueConstraint("name", name="otc_localauthority_name_5e53a784_uniq"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    ui_lta_id: Mapped[Optional[int]] = mapped_column(Integer)

    ui_lta: Mapped[Optional["UiLta"]] = relationship(
        "UiLta", back_populates="otc_localauthority"
    )
    otc_localauthority_registration_numbers: Mapped[
        List["OtcLocalauthorityRegistrationNumbers"]
    ] = relationship(
        "OtcLocalauthorityRegistrationNumbers", back_populates="localauthority"
    )


class OtcService(Base):
    __tablename__ = "otc_service"
    __table_args__ = (
        ForeignKeyConstraint(
            ["licence_id"],
            ["otc_licence.id"],
            deferrable=True,
            initially="DEFERRED",
            name="otc_service_licence_id_8b93ea5f_fk_otc_licence_id",
        ),
        ForeignKeyConstraint(
            ["operator_id"],
            ["otc_operator.id"],
            deferrable=True,
            initially="DEFERRED",
            name="otc_service_operator_id_26fe49fe_fk_otc_operator_id",
        ),
        PrimaryKeyConstraint("id", name="otc_service_pkey"),
    )

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

    licence: Mapped[Optional["OtcLicence"]] = relationship(
        "OtcLicence", back_populates="otc_service"
    )
    operator: Mapped[Optional["OtcOperator"]] = relationship(
        "OtcOperator", back_populates="otc_service"
    )
    otc_localauthority_registration_numbers: Mapped[
        List["OtcLocalauthorityRegistrationNumbers"]
    ] = relationship("OtcLocalauthorityRegistrationNumbers", back_populates="service")


class PipelinesDatasetetlerror(Base):
    __tablename__ = "pipelines_datasetetlerror"
    __table_args__ = (
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="pipelines_datasetetl_revision_id_d3d8c5ff_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="pipelines_datasetetlerrors_pkey"),
    )

    id: Mapped[int] = mapped_column(
        Integer, Sequence("pipelines_datasetetlerrors_id_seq"), primary_key=True
    )
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    severity: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(8096))
    revision_id: Mapped[Optional[int]] = mapped_column(Integer)

    revision: Mapped[Optional["OrganisationDatasetrevision"]] = relationship(
        "OrganisationDatasetrevision", back_populates="pipelines_datasetetlerror"
    )


class PipelinesDatasetetltaskresult(Base):
    __tablename__ = "pipelines_datasetetltaskresult"
    __table_args__ = (
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="pipelines_datasetetl_revision_id_9f9d619c_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="pipelines_datasetetltaskresult_pkey"),
        UniqueConstraint("task_id", name="pipelines_datasetetltaskresult_task_id_key"),
    )

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

    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision", back_populates="pipelines_datasetetltaskresult"
    )


class PipelinesFileprocessingresult(Base):
    __tablename__ = "pipelines_fileprocessingresult"
    __table_args__ = (
        ForeignKeyConstraint(
            ["pipeline_error_code_id"],
            ["pipelines_pipelineerrorcode.id"],
            deferrable=True,
            initially="DEFERRED",
            name="pipelines_fileproces_pipeline_error_code__90e865f3_fk_pipelines",
        ),
        ForeignKeyConstraint(
            ["pipeline_processing_step_id"],
            ["pipelines_pipelineprocessingstep.id"],
            deferrable=True,
            initially="DEFERRED",
            name="pipelines_fileproces_pipeline_processing__97aa79bd_fk_pipelines",
        ),
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="pipelines_fileproces_revision_id_9ecfda53_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="pipelines_fileprocessingresult_pkey"),
        UniqueConstraint("task_id", name="pipelines_fileprocessingresult_task_id_key"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
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

    pipeline_error_code: Mapped[Optional["PipelinesPipelineerrorcode"]] = relationship(
        "PipelinesPipelineerrorcode", back_populates="pipelines_fileprocessingresult"
    )
    pipeline_processing_step: Mapped["PipelinesPipelineprocessingstep"] = relationship(
        "PipelinesPipelineprocessingstep",
        back_populates="pipelines_fileprocessingresult",
    )
    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision", back_populates="pipelines_fileprocessingresult"
    )


class PipelinesRemotedatasethealthcheckcount(Base):
    __tablename__ = "pipelines_remotedatasethealthcheckcount"
    __table_args__ = (
        CheckConstraint(
            "count >= 0", name="pipelines_remotedatasethealthcheckcount_count_check"
        ),
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="pipelines_remotedata_revision_id_924d54b5_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="pipelines_remotedatasethealthcheckcount_pkey"),
        UniqueConstraint(
            "revision_id",
            name="pipelines_remotedatasethealthcheckcount_revision_id_key",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    count: Mapped[int] = mapped_column(Integer)
    revision_id: Mapped[int] = mapped_column(Integer)

    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision",
        back_populates="pipelines_remotedatasethealthcheckcount",
    )


class RestrictSessionsLoggedinuser(Base):
    __tablename__ = "restrict_sessions_loggedinuser"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="restrict_sessions_lo_user_id_e87e08a9_fk_users_use",
        ),
        PrimaryKeyConstraint("id", name="restrict_sessions_loggedinuser_pkey"),
        UniqueConstraint("user_id", name="restrict_sessions_loggedinuser_user_id_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    session_key: Mapped[Optional[str]] = mapped_column(String(32))

    user: Mapped["UsersUser"] = relationship(
        "UsersUser", back_populates="restrict_sessions_loggedinuser"
    )


class SiteAdminApirequest(Base):
    __tablename__ = "site_admin_apirequest"
    __table_args__ = (
        ForeignKeyConstraint(
            ["requestor_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="site_admin_apirequest_requestor_id_d5c386c3_fk_users_user_id",
        ),
        PrimaryKeyConstraint("id", name="site_admin_apirequest_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    path_info: Mapped[str] = mapped_column(String(512))
    query_string: Mapped[str] = mapped_column(String(512))
    requestor_id: Mapped[int] = mapped_column(Integer)

    requestor: Mapped["UsersUser"] = relationship(
        "UsersUser", back_populates="site_admin_apirequest"
    )


class SiteAdminResourcerequestcounter(Base):
    __tablename__ = "site_admin_resourcerequestcounter"
    __table_args__ = (
        ForeignKeyConstraint(
            ["requestor_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="site_admin_resourcer_requestor_id_44ebb90d_fk_users_use",
        ),
        PrimaryKeyConstraint("id", name="site_admin_resourcerequestcounter_pkey"),
        UniqueConstraint(
            "date",
            "requestor_id",
            "path_info",
            name="requestcounter_unique_with_requestor",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date)
    path_info: Mapped[str] = mapped_column(String(512))
    counter: Mapped[int] = mapped_column(Integer)
    requestor_id: Mapped[Optional[int]] = mapped_column(Integer)

    requestor: Mapped[Optional["UsersUser"]] = relationship(
        "UsersUser", back_populates="site_admin_resourcerequestcounter"
    )


class TransmodelServicepattern(Base):
    __tablename__ = "transmodel_servicepattern"
    __table_args__ = (
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_servicepa_revision_id_6917ba40_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="transmodel_servicepattern_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_pattern_id: Mapped[str] = mapped_column(String(255))
    origin: Mapped[str] = mapped_column(String(255))
    destination: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    geom: Mapped[Optional[Any]] = mapped_column(
        Geometry("LINESTRING", 4326, from_text="ST_GeomFromEWKT", name="geometry")
    )
    revision_id: Mapped[Optional[int]] = mapped_column(Integer)
    line_name: Mapped[Optional[str]] = mapped_column(String(255))

    revision: Mapped[Optional["OrganisationDatasetrevision"]] = relationship(
        "OrganisationDatasetrevision", back_populates="transmodel_servicepattern"
    )
    transmodel_vehiclejourney: Mapped[List["TransmodelVehiclejourney"]] = relationship(
        "TransmodelVehiclejourney", back_populates="service_pattern"
    )
    organisation_consumerfeedback: Mapped[List["OrganisationConsumerfeedback"]] = (
        relationship("OrganisationConsumerfeedback", back_populates="service_pattern")
    )


class TransmodelServicepatternServiceLinks(Base):
    __tablename__ = "transmodel_servicepattern_service_links"
    __table_args__ = (
        ForeignKeyConstraint(
            ["servicelink_id"],
            ["transmodel_servicelink.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_servicepa_servicelink_id_6a703624_fk_transmode",
        ),
        PrimaryKeyConstraint("id", name="transmodel_servicepattern_service_links_pkey"),
        UniqueConstraint(
            "servicepattern_id",
            "servicelink_id",
            name="transmodel_servicepatter_servicepattern_id_servic_a233ef3e_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    servicepattern_id: Mapped[int] = mapped_column(Integer)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    servicelink: Mapped["TransmodelServicelink"] = relationship(
        "TransmodelServicelink",
        back_populates="transmodel_servicepattern_service_links",
    )


class UsersUserGroups(Base):
    __tablename__ = "users_user_groups"
    __table_args__ = (
        ForeignKeyConstraint(
            ["group_id"],
            ["auth_group.id"],
            deferrable=True,
            initially="DEFERRED",
            name="users_user_groups_group_id_9afc8d0e_fk_auth_group_id",
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="users_user_groups_user_id_5f6f5a90_fk_users_user_id",
        ),
        PrimaryKeyConstraint("id", name="users_user_groups_pkey"),
        UniqueConstraint(
            "user_id",
            "group_id",
            name="users_user_groups_user_id_group_id_b88eab82_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    group_id: Mapped[int] = mapped_column(Integer)

    group: Mapped["AuthGroup"] = relationship(
        "AuthGroup", back_populates="users_user_groups"
    )
    user: Mapped["UsersUser"] = relationship(
        "UsersUser", back_populates="users_user_groups"
    )


class UsersUsersettings(UsersUser):
    __tablename__ = "users_usersettings"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="users_usersettings_user_id_401eaa29_fk_users_user_id",
        ),
        PrimaryKeyConstraint("user_id", name="users_usersettings_pkey"),
    )

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
    __tablename__ = "waffle_flag_groups"
    __table_args__ = (
        ForeignKeyConstraint(
            ["flag_id"],
            ["waffle_flag.id"],
            deferrable=True,
            initially="DEFERRED",
            name="waffle_flag_groups_flag_id_c11c0c05_fk_waffle_flag_id",
        ),
        ForeignKeyConstraint(
            ["group_id"],
            ["auth_group.id"],
            deferrable=True,
            initially="DEFERRED",
            name="waffle_flag_groups_group_id_a97c4f66_fk_auth_group_id",
        ),
        PrimaryKeyConstraint("id", name="waffle_flag_groups_pkey"),
        UniqueConstraint(
            "flag_id",
            "group_id",
            name="waffle_flag_groups_flag_id_group_id_8ba0c71b_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    flag_id: Mapped[int] = mapped_column(Integer)
    group_id: Mapped[int] = mapped_column(Integer)

    flag: Mapped["WaffleFlag"] = relationship(
        "WaffleFlag", back_populates="waffle_flag_groups"
    )
    group: Mapped["AuthGroup"] = relationship(
        "AuthGroup", back_populates="waffle_flag_groups"
    )


class WaffleFlagUsers(Base):
    __tablename__ = "waffle_flag_users"
    __table_args__ = (
        ForeignKeyConstraint(
            ["flag_id"],
            ["waffle_flag.id"],
            deferrable=True,
            initially="DEFERRED",
            name="waffle_flag_users_flag_id_833c37b0_fk_waffle_flag_id",
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="waffle_flag_users_user_id_8026df9b_fk_users_user_id",
        ),
        PrimaryKeyConstraint("id", name="waffle_flag_users_pkey"),
        UniqueConstraint(
            "flag_id", "user_id", name="waffle_flag_users_flag_id_user_id_b46f76b0_uniq"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    flag_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)

    flag: Mapped["WaffleFlag"] = relationship(
        "WaffleFlag", back_populates="waffle_flag_users"
    )
    user: Mapped["UsersUser"] = relationship(
        "UsersUser", back_populates="waffle_flag_users"
    )


class AccountEmailconfirmation(Base):
    __tablename__ = "account_emailconfirmation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["email_address_id"],
            ["account_emailaddress.id"],
            deferrable=True,
            initially="DEFERRED",
            name="account_emailconfirm_email_address_id_5b7f8c58_fk_account_e",
        ),
        PrimaryKeyConstraint("id", name="account_emailconfirmation_pkey"),
        UniqueConstraint("key", name="account_emailconfirmation_key_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    key: Mapped[str] = mapped_column(String(64))
    email_address_id: Mapped[int] = mapped_column(Integer)
    sent: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    email_address: Mapped["AccountEmailaddress"] = relationship(
        "AccountEmailaddress", back_populates="account_emailconfirmation"
    )


class AuthGroupPermissions(Base):
    __tablename__ = "auth_group_permissions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["group_id"],
            ["auth_group.id"],
            deferrable=True,
            initially="DEFERRED",
            name="auth_group_permissions_group_id_b120cbf9_fk_auth_group_id",
        ),
        ForeignKeyConstraint(
            ["permission_id"],
            ["auth_permission.id"],
            deferrable=True,
            initially="DEFERRED",
            name="auth_group_permissio_permission_id_84c5c92e_fk_auth_perm",
        ),
        PrimaryKeyConstraint("id", name="auth_group_permissions_pkey"),
        UniqueConstraint(
            "group_id",
            "permission_id",
            name="auth_group_permissions_group_id_permission_id_0cd325b0_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer)
    permission_id: Mapped[int] = mapped_column(Integer)

    group: Mapped["AuthGroup"] = relationship(
        "AuthGroup", back_populates="auth_group_permissions"
    )
    permission: Mapped["AuthPermission"] = relationship(
        "AuthPermission", back_populates="auth_group_permissions"
    )


class DataQualityDataqualityreportsummary(Base):
    __tablename__ = "data_quality_dataqualityreportsummary"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_dataqua_report_id_ae70c606_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_dataqualityreportsummary_pkey"),
        UniqueConstraint(
            "report_id",
            name="data_quality_dataqualityreportsummary_report_id_ae70c606_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data: Mapped[dict] = mapped_column(JSONB)
    report_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport",
        back_populates="data_quality_dataqualityreportsummary",
    )


class DataQualityFastlinkwarning(Base):
    __tablename__ = "data_quality_fastlinkwarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_fastlin_report_id_f0594a38_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timing_pattern_id"],
            ["data_quality_timingpattern.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_fastlin_timing_pattern_id_3860acf4_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_fastlinkwarning_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport", back_populates="data_quality_fastlinkwarning"
    )
    timing_pattern: Mapped["DataQualityTimingpattern"] = relationship(
        "DataQualityTimingpattern", back_populates="data_quality_fastlinkwarning"
    )
    data_quality_fastlinkwarning_service_links: Mapped[
        List["DataQualityFastlinkwarningServiceLinks"]
    ] = relationship(
        "DataQualityFastlinkwarningServiceLinks", back_populates="fastlinkwarning"
    )
    data_quality_fastlinkwarning_timings: Mapped[
        List["DataQualityFastlinkwarningTimings"]
    ] = relationship(
        "DataQualityFastlinkwarningTimings", back_populates="fastlinkwarning"
    )


class DataQualityFasttimingwarning(Base):
    __tablename__ = "data_quality_fasttimingwarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_fasttim_report_id_ea292475_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timing_pattern_id"],
            ["data_quality_timingpattern.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_fasttim_timing_pattern_id_cc840b76_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_fasttimingwarning_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport", back_populates="data_quality_fasttimingwarning"
    )
    timing_pattern: Mapped["DataQualityTimingpattern"] = relationship(
        "DataQualityTimingpattern", back_populates="data_quality_fasttimingwarning"
    )
    data_quality_fasttimingwarning_service_links: Mapped[
        List["DataQualityFasttimingwarningServiceLinks"]
    ] = relationship(
        "DataQualityFasttimingwarningServiceLinks", back_populates="fasttimingwarning"
    )
    data_quality_fasttimingwarning_timings: Mapped[
        List["DataQualityFasttimingwarningTimings"]
    ] = relationship(
        "DataQualityFasttimingwarningTimings", back_populates="fasttimingwarning"
    )


class DataQualityIncorrectnocwarning(Base):
    __tablename__ = "data_quality_incorrectnocwarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_incorre_report_id_4c6d3ae6_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_incorrectnocwarning_pkey"),
        UniqueConstraint(
            "report_id",
            "noc",
            name="data_quality_incorrectnocwarning_report_id_noc_a6e0b69a_uniq",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    noc: Mapped[str] = mapped_column(Text)
    report_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport",
        back_populates="data_quality_incorrectnocwarning",
    )


class DataQualityJourneyconflictwarning(Base):
    __tablename__ = "data_quality_journeyconflictwarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["conflict_id"],
            ["data_quality_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_journey_conflict_id_5ca94178_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_journey_report_id_0cb8ad04_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["vehicle_journey_id"],
            ["data_quality_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_journey_vehicle_journey_id_c070ab52_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_journeyconflictwarning_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    conflict_id: Mapped[int] = mapped_column(Integer)
    report_id: Mapped[int] = mapped_column(Integer)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)

    conflict: Mapped["DataQualityVehiclejourney"] = relationship(
        "DataQualityVehiclejourney",
        foreign_keys=[conflict_id],
        back_populates="data_quality_journeyconflictwarning",
    )
    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport",
        back_populates="data_quality_journeyconflictwarning",
    )
    vehicle_journey: Mapped["DataQualityVehiclejourney"] = relationship(
        "DataQualityVehiclejourney",
        foreign_keys=[vehicle_journey_id],
        back_populates="data_quality_journeyconflictwarning_",
    )
    data_quality_journeyconflictwarning_stops: Mapped[
        List["DataQualityJourneyconflictwarningStops"]
    ] = relationship(
        "DataQualityJourneyconflictwarningStops",
        back_populates="journeyconflictwarning",
    )


class DataQualityJourneydaterangebackwardswarning(Base):
    __tablename__ = "data_quality_journeydaterangebackwardswarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_journey_report_id_f3da6ca9_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["vehicle_journey_id"],
            ["data_quality_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_journey_vehicle_journey_id_d478edb8_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_journeydaterangebackwardswarning_pkey"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    start: Mapped[datetime.date] = mapped_column(Date)
    end: Mapped[datetime.date] = mapped_column(Date)
    report_id: Mapped[int] = mapped_column(Integer)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport",
        back_populates="data_quality_journeydaterangebackwardswarning",
    )
    vehicle_journey: Mapped["DataQualityVehiclejourney"] = relationship(
        "DataQualityVehiclejourney",
        back_populates="data_quality_journeydaterangebackwardswarning",
    )


class DataQualityJourneyduplicatewarning(Base):
    __tablename__ = "data_quality_journeyduplicatewarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["duplicate_id"],
            ["data_quality_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_journey_duplicate_id_7bc899e1_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_journey_report_id_44688d41_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["vehicle_journey_id"],
            ["data_quality_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_journey_vehicle_journey_id_302065c8_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_journeyduplicatewarning_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)
    duplicate_id: Mapped[int] = mapped_column(Integer)

    duplicate: Mapped["DataQualityVehiclejourney"] = relationship(
        "DataQualityVehiclejourney",
        foreign_keys=[duplicate_id],
        back_populates="data_quality_journeyduplicatewarning",
    )
    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport",
        back_populates="data_quality_journeyduplicatewarning",
    )
    vehicle_journey: Mapped["DataQualityVehiclejourney"] = relationship(
        "DataQualityVehiclejourney",
        foreign_keys=[vehicle_journey_id],
        back_populates="data_quality_journeyduplicatewarning_",
    )


class DataQualityJourneystopinappropriatewarning(Base):
    __tablename__ = "data_quality_journeystopinappropriatewarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_journey_report_id_bfd822bb_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_journeystopinappropriatewarning_pkey"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    stop_type: Mapped[str] = mapped_column(Text)
    report_id: Mapped[int] = mapped_column(Integer)
    stop_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport",
        back_populates="data_quality_journeystopinappropriatewarning",
    )
    data_quality_journeystopinappropriatewarning_vehicle_journeys: Mapped[
        List["DataQualityJourneystopinappropriatewarningVehicleJourneys"]
    ] = relationship(
        "DataQualityJourneystopinappropriatewarningVehicleJourneys",
        back_populates="journeystopinappropriatewarning",
    )


class DataQualityJourneywithoutheadsignwarning(Base):
    __tablename__ = "data_quality_journeywithoutheadsignwarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_journey_report_id_ab4565cb_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["vehicle_journey_id"],
            ["data_quality_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_journey_vehicle_journey_id_2c83956d_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_journeywithoutheadsignwarning_pkey"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport",
        back_populates="data_quality_journeywithoutheadsignwarning",
    )
    vehicle_journey: Mapped["DataQualityVehiclejourney"] = relationship(
        "DataQualityVehiclejourney",
        back_populates="data_quality_journeywithoutheadsignwarning",
    )


class DataQualityLineexpiredwarning(Base):
    __tablename__ = "data_quality_lineexpiredwarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_lineexp_report_id_da9d2c79_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["service_id"],
            ["data_quality_service.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_lineexp_service_id_335ab893_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_lineexpiredwarning_pkey"),
        UniqueConstraint(
            "report_id",
            "service_id",
            name="data_quality_lineexpired_report_id_service_id_f5b1282f_uniq",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    service_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport", back_populates="data_quality_lineexpiredwarning"
    )
    service: Mapped["DataQualityService"] = relationship(
        "DataQualityService", back_populates="data_quality_lineexpiredwarning"
    )
    data_quality_lineexpiredwarning_vehicle_journeys: Mapped[
        List["DataQualityLineexpiredwarningVehicleJourneys"]
    ] = relationship(
        "DataQualityLineexpiredwarningVehicleJourneys",
        back_populates="lineexpiredwarning",
    )


class DataQualityLinemissingblockidwarning(Base):
    __tablename__ = "data_quality_linemissingblockidwarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_linemis_report_id_2335000c_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["service_id"],
            ["data_quality_service.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_linemis_service_id_61f24ecc_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_linemissingblockidwarning_pkey"),
        UniqueConstraint(
            "report_id",
            "service_id",
            name="data_quality_linemissing_report_id_service_id_15450b24_uniq",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    service_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport",
        back_populates="data_quality_linemissingblockidwarning",
    )
    service: Mapped["DataQualityService"] = relationship(
        "DataQualityService", back_populates="data_quality_linemissingblockidwarning"
    )
    data_quality_linemissingblockidwarning_vehicle_journeys: Mapped[
        List["DataQualityLinemissingblockidwarningVehicleJourneys"]
    ] = relationship(
        "DataQualityLinemissingblockidwarningVehicleJourneys",
        back_populates="linemissingblockidwarning",
    )


class DataQualityServiceReports(Base):
    __tablename__ = "data_quality_service_reports"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataqualityreport_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_service_dataqualityreport_id_64ae07eb_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["service_id"],
            ["data_quality_service.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_service_service_id_3a8d9a7b_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_service_reports_pkey"),
        UniqueConstraint(
            "service_id",
            "dataqualityreport_id",
            name="data_quality_service_rep_service_id_dataqualityre_3bfc387f_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_id: Mapped[int] = mapped_column(Integer)
    dataqualityreport_id: Mapped[int] = mapped_column(Integer)

    dataqualityreport: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport", back_populates="data_quality_service_reports"
    )
    service: Mapped["DataQualityService"] = relationship(
        "DataQualityService", back_populates="data_quality_service_reports"
    )


class DataQualityServicelinkmissingstopwarning(Base):
    __tablename__ = "data_quality_servicelinkmissingstopwarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_service_report_id_69b73b55_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_servicelinkmissingstopwarning_pkey"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    service_link_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport",
        back_populates="data_quality_servicelinkmissingstopwarning",
    )
    data_quality_servicelinkmissingstopwarning_stops: Mapped[
        List["DataQualityServicelinkmissingstopwarningStops"]
    ] = relationship(
        "DataQualityServicelinkmissingstopwarningStops",
        back_populates="servicelinkmissingstopwarning",
    )


class DataQualitySlowlinkwarning(Base):
    __tablename__ = "data_quality_slowlinkwarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_slowlin_report_id_a24c4362_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timing_pattern_id"],
            ["data_quality_timingpattern.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_slowlin_timing_pattern_id_076e51c5_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_slowlinkwarning_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport", back_populates="data_quality_slowlinkwarning"
    )
    timing_pattern: Mapped["DataQualityTimingpattern"] = relationship(
        "DataQualityTimingpattern", back_populates="data_quality_slowlinkwarning"
    )
    data_quality_slowlinkwarning_service_links: Mapped[
        List["DataQualitySlowlinkwarningServiceLinks"]
    ] = relationship(
        "DataQualitySlowlinkwarningServiceLinks", back_populates="slowlinkwarning"
    )
    data_quality_slowlinkwarning_timings: Mapped[
        List["DataQualitySlowlinkwarningTimings"]
    ] = relationship(
        "DataQualitySlowlinkwarningTimings", back_populates="slowlinkwarning"
    )


class DataQualitySlowtimingwarning(Base):
    __tablename__ = "data_quality_slowtimingwarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_slowtim_report_id_435b19a9_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timing_pattern_id"],
            ["data_quality_timingpattern.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_slowtim_timing_pattern_id_33c25296_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_slowtimingwarning_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport", back_populates="data_quality_slowtimingwarning"
    )
    timing_pattern: Mapped["DataQualityTimingpattern"] = relationship(
        "DataQualityTimingpattern", back_populates="data_quality_slowtimingwarning"
    )
    data_quality_slowtimingwarning_service_links: Mapped[
        List["DataQualitySlowtimingwarningServiceLinks"]
    ] = relationship(
        "DataQualitySlowtimingwarningServiceLinks", back_populates="slowtimingwarning"
    )
    data_quality_slowtimingwarning_timings: Mapped[
        List["DataQualitySlowtimingwarningTimings"]
    ] = relationship(
        "DataQualitySlowtimingwarningTimings", back_populates="slowtimingwarning"
    )


class DataQualityStopincorrecttypewarning(Base):
    __tablename__ = "data_quality_stopincorrecttypewarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_stopinc_report_id_f2e95a2d_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_stopincorrecttypewarning_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    stop_type: Mapped[str] = mapped_column(Text)
    report_id: Mapped[int] = mapped_column(Integer)
    stop_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport",
        back_populates="data_quality_stopincorrecttypewarning",
    )
    data_quality_stopincorrecttypewarning_service_patterns: Mapped[
        List["DataQualityStopincorrecttypewarningServicePatterns"]
    ] = relationship(
        "DataQualityStopincorrecttypewarningServicePatterns",
        back_populates="stopincorrecttypewarning",
    )


class DataQualityStopmissingnaptanwarning(Base):
    __tablename__ = "data_quality_stopmissingnaptanwarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_stopmis_report_id_268c4823_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_stopmissingnaptanwarning_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    stop_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport",
        back_populates="data_quality_stopmissingnaptanwarning",
    )
    data_quality_stopmissingnaptanwarning_service_patterns: Mapped[
        List["DataQualityStopmissingnaptanwarningServicePatterns"]
    ] = relationship(
        "DataQualityStopmissingnaptanwarningServicePatterns",
        back_populates="stopmissingnaptanwarning",
    )


class DataQualityTaskresults(Base):
    __tablename__ = "data_quality_taskresults"
    __table_args__ = (
        ForeignKeyConstraint(
            ["checks_id"],
            ["data_quality_checks.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_taskres_checks_id_13c28ffa_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["dataquality_report_id"],
            ["data_quality_report.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_taskres_dataquality_report_i_76db2891_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["transmodel_txcfileattributes_id"],
            ["organisation_txcfileattributes.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_taskres_transmodel_txcfileat_d0c5a8a9_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="data_quality_taskresults_pkey"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    status: Mapped[str] = mapped_column(String(64))
    message: Mapped[str] = mapped_column(Text)
    checks_id: Mapped[Optional[int]] = mapped_column(Integer)
    dataquality_report_id: Mapped[Optional[int]] = mapped_column(Integer)
    transmodel_txcfileattributes_id: Mapped[Optional[int]] = mapped_column(Integer)

    checks: Mapped[Optional["DataQualityChecks"]] = relationship(
        "DataQualityChecks", back_populates="data_quality_taskresults"
    )
    dataquality_report: Mapped[Optional["DataQualityReport"]] = relationship(
        "DataQualityReport", back_populates="data_quality_taskresults"
    )
    transmodel_txcfileattributes: Mapped[Optional["OrganisationTxcfileattributes"]] = (
        relationship(
            "OrganisationTxcfileattributes", back_populates="data_quality_taskresults"
        )
    )
    data_quality_observationresults: Mapped[List["DataQualityObservationresults"]] = (
        relationship("DataQualityObservationresults", back_populates="taskresults")
    )


class DataQualityTimingbackwardswarning(Base):
    __tablename__ = "data_quality_timingbackwardswarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["from_stop_id"],
            ["data_quality_timingpatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingb_from_stop_id_b1fcc7ea_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingb_report_id_4bace234_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timing_pattern_id"],
            ["data_quality_timingpattern.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingb_timing_pattern_id_42796e5b_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["to_stop_id"],
            ["data_quality_timingpatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingb_to_stop_id_0beeb9c4_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_timingbackwardswarning_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)
    from_stop_id: Mapped[int] = mapped_column(Integer)
    to_stop_id: Mapped[int] = mapped_column(Integer)

    from_stop: Mapped["DataQualityTimingpatternstop"] = relationship(
        "DataQualityTimingpatternstop",
        foreign_keys=[from_stop_id],
        back_populates="data_quality_timingbackwardswarning",
    )
    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport",
        back_populates="data_quality_timingbackwardswarning",
    )
    timing_pattern: Mapped["DataQualityTimingpattern"] = relationship(
        "DataQualityTimingpattern", back_populates="data_quality_timingbackwardswarning"
    )
    to_stop: Mapped["DataQualityTimingpatternstop"] = relationship(
        "DataQualityTimingpatternstop",
        foreign_keys=[to_stop_id],
        back_populates="data_quality_timingbackwardswarning_",
    )
    data_quality_timingbackwardswarning_service_links: Mapped[
        List["DataQualityTimingbackwardswarningServiceLinks"]
    ] = relationship(
        "DataQualityTimingbackwardswarningServiceLinks",
        back_populates="timingbackwardswarning",
    )
    data_quality_timingbackwardswarning_timings: Mapped[
        List["DataQualityTimingbackwardswarningTimings"]
    ] = relationship(
        "DataQualityTimingbackwardswarningTimings",
        back_populates="timingbackwardswarning",
    )


class DataQualityTimingdropoffwarning(Base):
    __tablename__ = "data_quality_timingdropoffwarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingd_report_id_307d4237_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timing_pattern_id"],
            ["data_quality_timingpattern.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingd_timing_pattern_id_7cd52c29_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_timingdropoffwarning_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport",
        back_populates="data_quality_timingdropoffwarning",
    )
    timing_pattern: Mapped["DataQualityTimingpattern"] = relationship(
        "DataQualityTimingpattern", back_populates="data_quality_timingdropoffwarning"
    )
    data_quality_timingdropoffwarning_service_links: Mapped[
        List["DataQualityTimingdropoffwarningServiceLinks"]
    ] = relationship(
        "DataQualityTimingdropoffwarningServiceLinks",
        back_populates="timingdropoffwarning",
    )
    data_quality_timingdropoffwarning_timings: Mapped[
        List["DataQualityTimingdropoffwarningTimings"]
    ] = relationship(
        "DataQualityTimingdropoffwarningTimings", back_populates="timingdropoffwarning"
    )


class DataQualityTimingfirstwarning(Base):
    __tablename__ = "data_quality_timingfirstwarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingf_report_id_adfc9be6_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timing_pattern_id"],
            ["data_quality_timingpattern.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingf_timing_pattern_id_1c601a43_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_timingfirstwarning_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport", back_populates="data_quality_timingfirstwarning"
    )
    timing_pattern: Mapped["DataQualityTimingpattern"] = relationship(
        "DataQualityTimingpattern", back_populates="data_quality_timingfirstwarning"
    )
    data_quality_timingfirstwarning_service_links: Mapped[
        List["DataQualityTimingfirstwarningServiceLinks"]
    ] = relationship(
        "DataQualityTimingfirstwarningServiceLinks", back_populates="timingfirstwarning"
    )
    data_quality_timingfirstwarning_timings: Mapped[
        List["DataQualityTimingfirstwarningTimings"]
    ] = relationship(
        "DataQualityTimingfirstwarningTimings", back_populates="timingfirstwarning"
    )


class DataQualityTiminglastwarning(Base):
    __tablename__ = "data_quality_timinglastwarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingl_report_id_90ae5cdc_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timing_pattern_id"],
            ["data_quality_timingpattern.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingl_timing_pattern_id_a6d0af39_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_timinglastwarning_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport", back_populates="data_quality_timinglastwarning"
    )
    timing_pattern: Mapped["DataQualityTimingpattern"] = relationship(
        "DataQualityTimingpattern", back_populates="data_quality_timinglastwarning"
    )
    data_quality_timinglastwarning_service_links: Mapped[
        List["DataQualityTiminglastwarningServiceLinks"]
    ] = relationship(
        "DataQualityTiminglastwarningServiceLinks", back_populates="timinglastwarning"
    )
    data_quality_timinglastwarning_timings: Mapped[
        List["DataQualityTiminglastwarningTimings"]
    ] = relationship(
        "DataQualityTiminglastwarningTimings", back_populates="timinglastwarning"
    )


class DataQualityTimingmissingpointwarning(Base):
    __tablename__ = "data_quality_timingmissingpointwarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingm_report_id_3c176943_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timing_pattern_id"],
            ["data_quality_timingpattern.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingm_timing_pattern_id_3ed55093_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_timingmissingpointwarning_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport",
        back_populates="data_quality_timingmissingpointwarning",
    )
    timing_pattern: Mapped["DataQualityTimingpattern"] = relationship(
        "DataQualityTimingpattern",
        back_populates="data_quality_timingmissingpointwarning",
    )
    data_quality_timingmissingpointwarning_service_links: Mapped[
        List["DataQualityTimingmissingpointwarningServiceLinks"]
    ] = relationship(
        "DataQualityTimingmissingpointwarningServiceLinks",
        back_populates="timingmissingpointwarning",
    )
    data_quality_timingmissingpointwarning_timings: Mapped[
        List["DataQualityTimingmissingpointwarningTimings"]
    ] = relationship(
        "DataQualityTimingmissingpointwarningTimings",
        back_populates="timingmissingpointwarning",
    )


class DataQualityTimingmultiplewarning(Base):
    __tablename__ = "data_quality_timingmultiplewarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingm_report_id_189bc39a_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timing_pattern_id"],
            ["data_quality_timingpattern.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingm_timing_pattern_id_bbdf91e1_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_timingmultiplewarning_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport",
        back_populates="data_quality_timingmultiplewarning",
    )
    timing_pattern: Mapped["DataQualityTimingpattern"] = relationship(
        "DataQualityTimingpattern", back_populates="data_quality_timingmultiplewarning"
    )
    data_quality_timingmultiplewarning_timings: Mapped[
        List["DataQualityTimingmultiplewarningTimings"]
    ] = relationship(
        "DataQualityTimingmultiplewarningTimings",
        back_populates="timingmultiplewarning",
    )


class DataQualityTimingpickupwarning(Base):
    __tablename__ = "data_quality_timingpickupwarning"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingp_report_id_496c901d_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timing_pattern_id"],
            ["data_quality_timingpattern.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingp_timing_pattern_id_73b002a4_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_timingpickupwarning_pkey"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    report_id: Mapped[int] = mapped_column(Integer)
    timing_pattern_id: Mapped[int] = mapped_column(Integer)

    report: Mapped["DataQualityDataqualityreport"] = relationship(
        "DataQualityDataqualityreport",
        back_populates="data_quality_timingpickupwarning",
    )
    timing_pattern: Mapped["DataQualityTimingpattern"] = relationship(
        "DataQualityTimingpattern", back_populates="data_quality_timingpickupwarning"
    )
    data_quality_timingpickupwarning_service_links: Mapped[
        List["DataQualityTimingpickupwarningServiceLinks"]
    ] = relationship(
        "DataQualityTimingpickupwarningServiceLinks",
        back_populates="timingpickupwarning",
    )
    data_quality_timingpickupwarning_timings: Mapped[
        List["DataQualityTimingpickupwarningTimings"]
    ] = relationship(
        "DataQualityTimingpickupwarningTimings", back_populates="timingpickupwarning"
    )


class DqsTaskresults(Base):
    __tablename__ = "dqs_taskresults"
    __table_args__ = (
        ForeignKeyConstraint(
            ["checks_id"],
            ["dqs_checks.id"],
            deferrable=True,
            initially="DEFERRED",
            name="dqs_taskresults_checks_id_a474fbd2_fk_dqs_checks_id",
        ),
        ForeignKeyConstraint(
            ["dataquality_report_id"],
            ["dqs_report.id"],
            deferrable=True,
            initially="DEFERRED",
            name="dqs_taskresults_dataquality_report_id_b3cfb422_fk_dqs_report_id",
        ),
        ForeignKeyConstraint(
            ["transmodel_txcfileattributes_id"],
            ["organisation_txcfileattributes.id"],
            deferrable=True,
            initially="DEFERRED",
            name="dqs_taskresults_transmodel_txcfileat_36d8a29c_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="dqs_taskresults_pkey"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    status: Mapped[str] = mapped_column(String(64))
    message: Mapped[str] = mapped_column(Text)
    checks_id: Mapped[Optional[int]] = mapped_column(Integer)
    dataquality_report_id: Mapped[Optional[int]] = mapped_column(Integer)
    transmodel_txcfileattributes_id: Mapped[Optional[int]] = mapped_column(Integer)

    checks: Mapped[Optional["DqsChecks"]] = relationship(
        "DqsChecks", back_populates="dqs_taskresults"
    )
    dataquality_report: Mapped[Optional["DqsReport"]] = relationship(
        "DqsReport", back_populates="dqs_taskresults"
    )
    transmodel_txcfileattributes: Mapped[Optional["OrganisationTxcfileattributes"]] = (
        relationship("OrganisationTxcfileattributes", back_populates="dqs_taskresults")
    )
    dqs_observationresults: Mapped[List["DqsObservationresults"]] = relationship(
        "DqsObservationresults", back_populates="taskresults"
    )


class FaresFaresmetadata(OrganisationDatasetmetadata):
    __tablename__ = "fares_faresmetadata"
    __table_args__ = (
        CheckConstraint(
            "num_of_fare_products >= 0",
            name="fares_faresmetadata_num_of_fare_products_check",
        ),
        CheckConstraint(
            "num_of_fare_zones >= 0", name="fares_faresmetadata_num_of_fare_zones_check"
        ),
        CheckConstraint(
            "num_of_lines >= 0", name="fares_faresmetadata_num_of_lines_check"
        ),
        CheckConstraint(
            "num_of_pass_products >= 0",
            name="fares_faresmetadata_num_of_pass_products_check",
        ),
        CheckConstraint(
            "num_of_sales_offer_packages >= 0",
            name="fares_faresmetadata_num_of_sales_offer_packages_check",
        ),
        CheckConstraint(
            "num_of_trip_products >= 0",
            name="fares_faresmetadata_num_of_trip_products_check",
        ),
        CheckConstraint(
            "num_of_user_profiles >= 0",
            name="fares_faresmetadata_num_of_user_profiles_check",
        ),
        ForeignKeyConstraint(
            ["datasetmetadata_ptr_id"],
            ["organisation_datasetmetadata.id"],
            deferrable=True,
            initially="DEFERRED",
            name="fares_faresmetadata_datasetmetadata_ptr__7a173a37_fk_organisat",
        ),
        PrimaryKeyConstraint("datasetmetadata_ptr_id", name="fares_faresmetadata_pkey"),
    )

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

    fares_datacataloguemetadata: Mapped[List["FaresDatacataloguemetadata"]] = (
        relationship("FaresDatacataloguemetadata", back_populates="fares_metadata")
    )
    fares_faresmetadata_stops: Mapped[List["FaresFaresmetadataStops"]] = relationship(
        "FaresFaresmetadataStops", back_populates="faresmetadata"
    )


class FaresValidatorFaresvalidation(Base):
    __tablename__ = "fares_validator_faresvalidation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organisation_id"],
            ["organisation_organisation.id"],
            deferrable=True,
            initially="DEFERRED",
            name="fares_validator_fare_organisation_id_0e21dd87_fk_organisat",
        ),
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="fares_validator_fare_revision_id_50166752_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="fares_validator_faresvalidation_pkey"),
    )

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

    organisation: Mapped["OrganisationOrganisation"] = relationship(
        "OrganisationOrganisation", back_populates="fares_validator_faresvalidation"
    )
    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision", back_populates="fares_validator_faresvalidation"
    )


class FaresValidatorFaresvalidationresult(Base):
    __tablename__ = "fares_validator_faresvalidationresult"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organisation_id"],
            ["organisation_organisation.id"],
            deferrable=True,
            initially="DEFERRED",
            name="fares_validator_fare_organisation_id_66165e76_fk_organisat",
        ),
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="fares_validator_fare_revision_id_566d0ffa_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="fares_validator_faresvalidationresult_pkey"),
        UniqueConstraint(
            "revision_id", name="fares_validator_faresvalidationresult_revision_id_key"
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    count: Mapped[int] = mapped_column(Integer)
    report_file_name: Mapped[str] = mapped_column(String(256))
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    organisation_id: Mapped[int] = mapped_column(Integer)
    revision_id: Mapped[int] = mapped_column(Integer)

    organisation: Mapped["OrganisationOrganisation"] = relationship(
        "OrganisationOrganisation",
        back_populates="fares_validator_faresvalidationresult",
    )
    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision",
        back_populates="fares_validator_faresvalidationresult",
    )


class NaptanLocality(Base):
    __tablename__ = "naptan_locality"
    __table_args__ = (
        ForeignKeyConstraint(
            ["admin_area_id"],
            ["naptan_adminarea.id"],
            deferrable=True,
            initially="DEFERRED",
            name="naptan_locality_admin_area_id_0765cd72_fk_naptan_adminarea_id",
        ),
        ForeignKeyConstraint(
            ["district_id"],
            ["naptan_district.id"],
            deferrable=True,
            initially="DEFERRED",
            name="naptan_locality_district_id_39815ea9_fk_naptan_district_id",
        ),
        PrimaryKeyConstraint("gazetteer_id", name="naptan_locality_pkey"),
    )

    gazetteer_id: Mapped[str] = mapped_column(String(8), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    easting: Mapped[int] = mapped_column(Integer)
    northing: Mapped[int] = mapped_column(Integer)
    admin_area_id: Mapped[Optional[int]] = mapped_column(Integer)
    district_id: Mapped[Optional[int]] = mapped_column(Integer)

    admin_area: Mapped[Optional["NaptanAdminarea"]] = relationship(
        "NaptanAdminarea", back_populates="naptan_locality"
    )
    district: Mapped[Optional["NaptanDistrict"]] = relationship(
        "NaptanDistrict", back_populates="naptan_locality"
    )
    naptan_stoppoint: Mapped[List["NaptanStoppoint"]] = relationship(
        "NaptanStoppoint", back_populates="locality"
    )
    organisation_datasetrevision_localities: Mapped[
        List["OrganisationDatasetrevisionLocalities"]
    ] = relationship("OrganisationDatasetrevisionLocalities", back_populates="locality")
    transmodel_servicepattern_localities: Mapped[
        List["TransmodelServicepatternLocalities"]
    ] = relationship("TransmodelServicepatternLocalities", back_populates="locality")


class OrganisationConsumerstats(Base):
    __tablename__ = "organisation_consumerstats"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organisation_id"],
            ["organisation_organisation.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_consume_organisation_id_f98a7a45_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="organisation_consumerstats_pkey"),
        UniqueConstraint(
            "organisation_id", name="organisation_consumerstats_organisation_id_key"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    monthly_breakdown: Mapped[str] = mapped_column(String(100))
    weekly_unique_consumers: Mapped[int] = mapped_column(Integer)
    weekly_downloads: Mapped[int] = mapped_column(Integer)
    weekly_api_hits: Mapped[int] = mapped_column(Integer)
    organisation_id: Mapped[int] = mapped_column(Integer)

    organisation: Mapped["OrganisationOrganisation"] = relationship(
        "OrganisationOrganisation", back_populates="organisation_consumerstats"
    )


class OrganisationDatasetrevisionAdminAreas(Base):
    __tablename__ = "organisation_datasetrevision_admin_areas"
    __table_args__ = (
        ForeignKeyConstraint(
            ["adminarea_id"],
            ["naptan_adminarea.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_dataset_adminarea_id_8e172fe4_fk_naptan_ad",
        ),
        ForeignKeyConstraint(
            ["datasetrevision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_dataset_datasetrevision_id_bfc0fd88_fk_organisat",
        ),
        PrimaryKeyConstraint(
            "id", name="organisation_datasetrevision_admin_areas_pkey"
        ),
        UniqueConstraint(
            "datasetrevision_id",
            "adminarea_id",
            name="organisation_datasetrevi_datasetrevision_id_admin_4188ea15_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    datasetrevision_id: Mapped[int] = mapped_column(Integer)
    adminarea_id: Mapped[int] = mapped_column(Integer)

    adminarea: Mapped["NaptanAdminarea"] = relationship(
        "NaptanAdminarea", back_populates="organisation_datasetrevision_admin_areas"
    )
    datasetrevision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision",
        back_populates="organisation_datasetrevision_admin_areas",
    )


class OrganisationLicence(Base):
    __tablename__ = "organisation_licence"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organisation_id"],
            ["organisation_organisation.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_licence_organisation_id_9de67053_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="organisation_licence_pkey"),
        UniqueConstraint("number", name="organisation_licence_number_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(9))
    organisation_id: Mapped[int] = mapped_column(Integer)

    organisation: Mapped["OrganisationOrganisation"] = relationship(
        "OrganisationOrganisation", back_populates="organisation_licence"
    )
    organisation_seasonalservice: Mapped[List["OrganisationSeasonalservice"]] = (
        relationship("OrganisationSeasonalservice", back_populates="licence")
    )
    organisation_servicecodeexemption: Mapped[
        List["OrganisationServicecodeexemption"]
    ] = relationship("OrganisationServicecodeexemption", back_populates="licence")


class OrganisationOperatorcode(Base):
    __tablename__ = "organisation_operatorcode"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organisation_id"],
            ["organisation_organisation.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_operato_organisation_id_854edcec_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="organisation_operatorcode_pkey"),
        UniqueConstraint("noc", name="organisation_operatorcode_noc_d6b5203e_uniq"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    noc: Mapped[str] = mapped_column(String(20))
    organisation_id: Mapped[int] = mapped_column(Integer)

    organisation: Mapped["OrganisationOrganisation"] = relationship(
        "OrganisationOrganisation", back_populates="organisation_operatorcode"
    )


class OrganisationOrganisationAdminAreas(Base):
    __tablename__ = "organisation_organisation_admin_areas"
    __table_args__ = (
        ForeignKeyConstraint(
            ["adminarea_id"],
            ["naptan_adminarea.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_organis_adminarea_id_87fab358_fk_naptan_ad",
        ),
        ForeignKeyConstraint(
            ["organisation_id"],
            ["organisation_organisation.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_organis_organisation_id_ffd3f6f0_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="organisation_organisation_admin_areas_pkey"),
        UniqueConstraint(
            "organisation_id",
            "adminarea_id",
            name="organisation_organisatio_organisation_id_adminare_80bdb5ce_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    organisation_id: Mapped[int] = mapped_column(Integer)
    adminarea_id: Mapped[int] = mapped_column(Integer)

    adminarea: Mapped["NaptanAdminarea"] = relationship(
        "NaptanAdminarea", back_populates="organisation_organisation_admin_areas"
    )
    organisation: Mapped["OrganisationOrganisation"] = relationship(
        "OrganisationOrganisation",
        back_populates="organisation_organisation_admin_areas",
    )


class OtcLocalauthorityRegistrationNumbers(Base):
    __tablename__ = "otc_localauthority_registration_numbers"
    __table_args__ = (
        ForeignKeyConstraint(
            ["localauthority_id"],
            ["otc_localauthority.id"],
            deferrable=True,
            initially="DEFERRED",
            name="otc_localauthority_r_localauthority_id_7b261027_fk_otc_local",
        ),
        ForeignKeyConstraint(
            ["service_id"],
            ["otc_service.id"],
            deferrable=True,
            initially="DEFERRED",
            name="otc_localauthority_r_service_id_75d70959_fk_otc_servi",
        ),
        PrimaryKeyConstraint("id", name="otc_localauthority_registration_numbers_pkey"),
        UniqueConstraint(
            "localauthority_id",
            "service_id",
            name="otc_localauthority_regis_localauthority_id_servic_708d1fe0_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    localauthority_id: Mapped[int] = mapped_column(Integer)
    service_id: Mapped[int] = mapped_column(Integer)

    localauthority: Mapped["OtcLocalauthority"] = relationship(
        "OtcLocalauthority", back_populates="otc_localauthority_registration_numbers"
    )
    service: Mapped["OtcService"] = relationship(
        "OtcService", back_populates="otc_localauthority_registration_numbers"
    )


class PipelinesDataqualitytask(Base):
    __tablename__ = "pipelines_dataqualitytask"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"],
            ["data_quality_dataqualityreport.id"],
            deferrable=True,
            initially="DEFERRED",
            name="pipelines_dataqualit_report_id_fa790536_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="pipelines_dataqualit_revision_id_a45d1a58_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="pipelines_dataqualitytask_pkey"),
        UniqueConstraint("report_id", name="pipelines_dataqualitytask_report_id_key"),
        UniqueConstraint(
            "task_id", name="pipelines_dataqualitytask_task_id_6d36756c_uniq"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    status: Mapped[str] = mapped_column(String(50))
    revision_id: Mapped[int] = mapped_column(Integer)
    message: Mapped[str] = mapped_column(Text)
    task_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    report_id: Mapped[Optional[int]] = mapped_column(Integer)
    completed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    report: Mapped[Optional["DataQualityDataqualityreport"]] = relationship(
        "DataQualityDataqualityreport", back_populates="pipelines_dataqualitytask"
    )
    revision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision", back_populates="pipelines_dataqualitytask"
    )


class TransmodelService(Base):
    __tablename__ = "transmodel_service"
    __table_args__ = (
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_service_revision_id_6a8e3139_fk_organisat",
        ),
        ForeignKeyConstraint(
            ["txcfileattributes_id"],
            ["organisation_txcfileattributes.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_service_txcfileattributes_id_7b93a5d9_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="transmodel_service_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_code: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    other_names: Mapped[list] = mapped_column(ARRAY(String(length=255)))
    start_date: Mapped[datetime.date] = mapped_column(Date)
    service_type: Mapped[str] = mapped_column(String(255))
    end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    revision_id: Mapped[Optional[int]] = mapped_column(Integer)
    txcfileattributes_id: Mapped[Optional[int]] = mapped_column(Integer)

    revision: Mapped[Optional["OrganisationDatasetrevision"]] = relationship(
        "OrganisationDatasetrevision", back_populates="transmodel_service"
    )
    txcfileattributes: Mapped[Optional["OrganisationTxcfileattributes"]] = relationship(
        "OrganisationTxcfileattributes", back_populates="transmodel_service"
    )
    transmodel_bookingarrangements: Mapped[List["TransmodelBookingarrangements"]] = (
        relationship("TransmodelBookingarrangements", back_populates="service")
    )
    transmodel_service_service_patterns: Mapped[
        List["TransmodelServiceServicePatterns"]
    ] = relationship("TransmodelServiceServicePatterns", back_populates="service")
    organisation_consumerfeedback: Mapped[List["OrganisationConsumerfeedback"]] = (
        relationship("OrganisationConsumerfeedback", back_populates="service")
    )


class TransmodelServicepatternAdminAreas(Base):
    __tablename__ = "transmodel_servicepattern_admin_areas"
    __table_args__ = (
        ForeignKeyConstraint(
            ["adminarea_id"],
            ["naptan_adminarea.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_servicepa_adminarea_id_97cdf952_fk_naptan_ad",
        ),
        PrimaryKeyConstraint("id", name="transmodel_servicepattern_admin_areas_pkey"),
        UniqueConstraint(
            "servicepattern_id",
            "adminarea_id",
            name="transmodel_servicepatter_servicepattern_id_admina_377fa39a_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    servicepattern_id: Mapped[int] = mapped_column(Integer)
    adminarea_id: Mapped[int] = mapped_column(Integer)

    adminarea: Mapped["NaptanAdminarea"] = relationship(
        "NaptanAdminarea", back_populates="transmodel_servicepattern_admin_areas"
    )


class TransmodelVehiclejourney(Base):
    __tablename__ = "transmodel_vehiclejourney"
    __table_args__ = (
        ForeignKeyConstraint(
            ["service_pattern_id"],
            ["transmodel_servicepattern.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_vehiclejo_service_pattern_id_1b8caece_fk_transmode",
        ),
        PrimaryKeyConstraint("id", name="transmodel_vehiclejourney_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    departure_day_shift: Mapped[bool] = mapped_column(Boolean)
    start_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    direction: Mapped[Optional[str]] = mapped_column(String(255))
    journey_code: Mapped[Optional[str]] = mapped_column(String(255))
    line_ref: Mapped[Optional[str]] = mapped_column(String(255))
    service_pattern_id: Mapped[Optional[int]] = mapped_column(Integer)
    block_number: Mapped[Optional[str]] = mapped_column(String(20))

    service_pattern: Mapped[Optional["TransmodelServicepattern"]] = relationship(
        "TransmodelServicepattern", back_populates="transmodel_vehiclejourney"
    )
    transmodel_flexibleserviceoperationperiod: Mapped[
        List["TransmodelFlexibleserviceoperationperiod"]
    ] = relationship(
        "TransmodelFlexibleserviceoperationperiod", back_populates="vehicle_journey"
    )
    transmodel_nonoperatingdatesexceptions: Mapped[
        List["TransmodelNonoperatingdatesexceptions"]
    ] = relationship(
        "TransmodelNonoperatingdatesexceptions", back_populates="vehicle_journey"
    )
    transmodel_operatingdatesexceptions: Mapped[
        List["TransmodelOperatingdatesexceptions"]
    ] = relationship(
        "TransmodelOperatingdatesexceptions", back_populates="vehicle_journey"
    )
    transmodel_operatingprofile: Mapped[List["TransmodelOperatingprofile"]] = (
        relationship("TransmodelOperatingprofile", back_populates="vehicle_journey")
    )
    transmodel_servicedorganisationvehiclejourney: Mapped[
        List["TransmodelServicedorganisationvehiclejourney"]
    ] = relationship(
        "TransmodelServicedorganisationvehiclejourney", back_populates="vehicle_journey"
    )
    transmodel_servicepatternstop: Mapped[List["TransmodelServicepatternstop"]] = (
        relationship("TransmodelServicepatternstop", back_populates="vehicle_journey")
    )
    transmodel_tracksvehiclejourney: Mapped[List["TransmodelTracksvehiclejourney"]] = (
        relationship("TransmodelTracksvehiclejourney", back_populates="vehicle_journey")
    )
    data_quality_observationresults: Mapped[List["DataQualityObservationresults"]] = (
        relationship("DataQualityObservationresults", back_populates="vehicle_journey")
    )
    dqs_observationresults: Mapped[List["DqsObservationresults"]] = relationship(
        "DqsObservationresults", back_populates="vehicle_journey"
    )
    organisation_consumerfeedback: Mapped[List["OrganisationConsumerfeedback"]] = (
        relationship("OrganisationConsumerfeedback", back_populates="vehicle_journey")
    )


class UsersInvitation(InvitationsInvitation):
    __tablename__ = "users_invitation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["invitation_ptr_id"],
            ["invitations_invitation.id"],
            deferrable=True,
            initially="DEFERRED",
            name="users_invitation_invitation_ptr_id_4299c269_fk",
        ),
        ForeignKeyConstraint(
            ["organisation_id"],
            ["organisation_organisation.id"],
            deferrable=True,
            initially="DEFERRED",
            name="users_invitation_organisation_id_e4c94813_fk_organisat",
        ),
        PrimaryKeyConstraint("invitation_ptr_id", name="users_invitation_pkey"),
    )

    invitation_ptr_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    account_type: Mapped[int] = mapped_column(Integer)
    is_key_contact: Mapped[bool] = mapped_column(Boolean)
    organisation_id: Mapped[Optional[int]] = mapped_column(Integer)

    organisation: Mapped[Optional["OrganisationOrganisation"]] = relationship(
        "OrganisationOrganisation", back_populates="users_invitation"
    )
    users_agentuserinvite: Mapped[Optional["UsersAgentuserinvite"]] = relationship(
        "UsersAgentuserinvite", uselist=False, back_populates="invitation"
    )


class UsersUserOrganisations(Base):
    __tablename__ = "users_user_organisations"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organisation_id"],
            ["organisation_organisation.id"],
            deferrable=True,
            initially="DEFERRED",
            name="users_user_organisat_organisation_id_57ef74c1_fk_organisat",
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="users_user_organisations_user_id_7709ae8f_fk_users_user_id",
        ),
        PrimaryKeyConstraint("id", name="users_user_organisations_pkey"),
        UniqueConstraint(
            "user_id",
            "organisation_id",
            name="users_user_organisations_user_id_organisation_id_0030e7a0_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    organisation_id: Mapped[int] = mapped_column(Integer)

    organisation: Mapped["OrganisationOrganisation"] = relationship(
        "OrganisationOrganisation", back_populates="users_user_organisations"
    )
    user: Mapped["UsersUser"] = relationship(
        "UsersUser", back_populates="users_user_organisations"
    )


class UsersUserUserPermissions(Base):
    __tablename__ = "users_user_user_permissions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["permission_id"],
            ["auth_permission.id"],
            deferrable=True,
            initially="DEFERRED",
            name="users_user_user_perm_permission_id_0b93982e_fk_auth_perm",
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="users_user_user_permissions_user_id_20aca447_fk_users_user_id",
        ),
        PrimaryKeyConstraint("id", name="users_user_user_permissions_pkey"),
        UniqueConstraint(
            "user_id",
            "permission_id",
            name="users_user_user_permissions_user_id_permission_id_43338c45_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    permission_id: Mapped[int] = mapped_column(Integer)

    permission: Mapped["AuthPermission"] = relationship(
        "AuthPermission", back_populates="users_user_user_permissions"
    )
    user: Mapped["UsersUser"] = relationship(
        "UsersUser", back_populates="users_user_user_permissions"
    )


class DataQualityFastlinkwarningServiceLinks(Base):
    __tablename__ = "data_quality_fastlinkwarning_service_links"
    __table_args__ = (
        ForeignKeyConstraint(
            ["fastlinkwarning_id"],
            ["data_quality_fastlinkwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_fastlin_fastlinkwarning_id_f50006b4_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_fastlinkwarning_service_links_pkey"
        ),
        UniqueConstraint(
            "fastlinkwarning_id",
            "servicelink_id",
            name="data_quality_fastlinkwar_fastlinkwarning_id_servi_865111f4_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fastlinkwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    fastlinkwarning: Mapped["DataQualityFastlinkwarning"] = relationship(
        "DataQualityFastlinkwarning",
        back_populates="data_quality_fastlinkwarning_service_links",
    )


class DataQualityFastlinkwarningTimings(Base):
    __tablename__ = "data_quality_fastlinkwarning_timings"
    __table_args__ = (
        ForeignKeyConstraint(
            ["fastlinkwarning_id"],
            ["data_quality_fastlinkwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_fastlin_fastlinkwarning_id_f8cf8247_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timingpatternstop_id"],
            ["data_quality_timingpatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_fastlin_timingpatternstop_id_76271554_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_fastlinkwarning_timings_pkey"),
        UniqueConstraint(
            "fastlinkwarning_id",
            "timingpatternstop_id",
            name="data_quality_fastlinkwar_fastlinkwarning_id_timin_a5084f81_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fastlinkwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    fastlinkwarning: Mapped["DataQualityFastlinkwarning"] = relationship(
        "DataQualityFastlinkwarning",
        back_populates="data_quality_fastlinkwarning_timings",
    )
    timingpatternstop: Mapped["DataQualityTimingpatternstop"] = relationship(
        "DataQualityTimingpatternstop",
        back_populates="data_quality_fastlinkwarning_timings",
    )


class DataQualityFasttimingwarningServiceLinks(Base):
    __tablename__ = "data_quality_fasttimingwarning_service_links"
    __table_args__ = (
        ForeignKeyConstraint(
            ["fasttimingwarning_id"],
            ["data_quality_fasttimingwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_fasttim_fasttimingwarning_id_ae58098b_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_fasttimingwarning_service_links_pkey"
        ),
        UniqueConstraint(
            "fasttimingwarning_id",
            "servicelink_id",
            name="data_quality_fasttimingw_fasttimingwarning_id_ser_689348f0_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fasttimingwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    fasttimingwarning: Mapped["DataQualityFasttimingwarning"] = relationship(
        "DataQualityFasttimingwarning",
        back_populates="data_quality_fasttimingwarning_service_links",
    )


class DataQualityFasttimingwarningTimings(Base):
    __tablename__ = "data_quality_fasttimingwarning_timings"
    __table_args__ = (
        ForeignKeyConstraint(
            ["fasttimingwarning_id"],
            ["data_quality_fasttimingwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_fasttim_fasttimingwarning_id_361feac9_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timingpatternstop_id"],
            ["data_quality_timingpatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_fasttim_timingpatternstop_id_003aeef5_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_fasttimingwarning_timings_pkey"),
        UniqueConstraint(
            "fasttimingwarning_id",
            "timingpatternstop_id",
            name="data_quality_fasttimingw_fasttimingwarning_id_tim_96bb78b1_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fasttimingwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    fasttimingwarning: Mapped["DataQualityFasttimingwarning"] = relationship(
        "DataQualityFasttimingwarning",
        back_populates="data_quality_fasttimingwarning_timings",
    )
    timingpatternstop: Mapped["DataQualityTimingpatternstop"] = relationship(
        "DataQualityTimingpatternstop",
        back_populates="data_quality_fasttimingwarning_timings",
    )


class DataQualityJourneyconflictwarningStops(Base):
    __tablename__ = "data_quality_journeyconflictwarning_stops"
    __table_args__ = (
        ForeignKeyConstraint(
            ["journeyconflictwarning_id"],
            ["data_quality_journeyconflictwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_journey_journeyconflictwarni_d6f1a896_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_journeyconflictwarning_stops_pkey"
        ),
        UniqueConstraint(
            "journeyconflictwarning_id",
            "stoppoint_id",
            name="data_quality_journeyconf_journeyconflictwarning_i_afa54caa_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    journeyconflictwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    stoppoint_id: Mapped[int] = mapped_column(Integer)

    journeyconflictwarning: Mapped["DataQualityJourneyconflictwarning"] = relationship(
        "DataQualityJourneyconflictwarning",
        back_populates="data_quality_journeyconflictwarning_stops",
    )


class DataQualityJourneystopinappropriatewarningVehicleJourneys(Base):
    __tablename__ = "data_quality_journeystopinappropriatewarning_vehicle_journeys"
    __table_args__ = (
        ForeignKeyConstraint(
            ["journeystopinappropriatewarning_id"],
            ["data_quality_journeystopinappropriatewarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_journey_journeystopinappropr_9660e2bf_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["vehiclejourney_id"],
            ["data_quality_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_journey_vehiclejourney_id_9b87d4ee_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_journeystopinappropriatewarning_vehicle_journ_pkey"
        ),
        UniqueConstraint(
            "journeystopinappropriatewarning_id",
            "vehiclejourney_id",
            name="data_quality_journeystop_journeystopinappropriate_e1efc373_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Sequence("data_quality_journeystopinappropriatewarning_vehicle_jou_id_seq"),
        primary_key=True,
    )
    journeystopinappropriatewarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    vehiclejourney_id: Mapped[int] = mapped_column(Integer)

    journeystopinappropriatewarning: Mapped[
        "DataQualityJourneystopinappropriatewarning"
    ] = relationship(
        "DataQualityJourneystopinappropriatewarning",
        back_populates="data_quality_journeystopinappropriatewarning_vehicle_journeys",
    )
    vehiclejourney: Mapped["DataQualityVehiclejourney"] = relationship(
        "DataQualityVehiclejourney",
        back_populates="data_quality_journeystopinappropriatewarning_vehicle_journeys",
    )


class DataQualityLineexpiredwarningVehicleJourneys(Base):
    __tablename__ = "data_quality_lineexpiredwarning_vehicle_journeys"
    __table_args__ = (
        ForeignKeyConstraint(
            ["lineexpiredwarning_id"],
            ["data_quality_lineexpiredwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_lineexp_lineexpiredwarning_i_72548d1f_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["vehiclejourney_id"],
            ["data_quality_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_lineexp_vehiclejourney_id_f1ddc8eb_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_lineexpiredwarning_vehicle_journeys_pkey"
        ),
        UniqueConstraint(
            "lineexpiredwarning_id",
            "vehiclejourney_id",
            name="data_quality_lineexpired_lineexpiredwarning_id_ve_a34d6dbc_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lineexpiredwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    vehiclejourney_id: Mapped[int] = mapped_column(Integer)

    lineexpiredwarning: Mapped["DataQualityLineexpiredwarning"] = relationship(
        "DataQualityLineexpiredwarning",
        back_populates="data_quality_lineexpiredwarning_vehicle_journeys",
    )
    vehiclejourney: Mapped["DataQualityVehiclejourney"] = relationship(
        "DataQualityVehiclejourney",
        back_populates="data_quality_lineexpiredwarning_vehicle_journeys",
    )


class DataQualityLinemissingblockidwarningVehicleJourneys(Base):
    __tablename__ = "data_quality_linemissingblockidwarning_vehicle_journeys"
    __table_args__ = (
        ForeignKeyConstraint(
            ["linemissingblockidwarning_id"],
            ["data_quality_linemissingblockidwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_linemis_linemissingblockidwa_95fc8a58_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["vehiclejourney_id"],
            ["data_quality_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_linemis_vehiclejourney_id_34070c98_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_linemissingblockidwarning_vehicle_journeys_pkey"
        ),
        UniqueConstraint(
            "linemissingblockidwarning_id",
            "vehiclejourney_id",
            name="data_quality_linemissing_linemissingblockidwarnin_38bb375d_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    linemissingblockidwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    vehiclejourney_id: Mapped[int] = mapped_column(Integer)

    linemissingblockidwarning: Mapped["DataQualityLinemissingblockidwarning"] = (
        relationship(
            "DataQualityLinemissingblockidwarning",
            back_populates="data_quality_linemissingblockidwarning_vehicle_journeys",
        )
    )
    vehiclejourney: Mapped["DataQualityVehiclejourney"] = relationship(
        "DataQualityVehiclejourney",
        back_populates="data_quality_linemissingblockidwarning_vehicle_journeys",
    )


class DataQualityServicelinkmissingstopwarningStops(Base):
    __tablename__ = "data_quality_servicelinkmissingstopwarning_stops"
    __table_args__ = (
        ForeignKeyConstraint(
            ["servicelinkmissingstopwarning_id"],
            ["data_quality_servicelinkmissingstopwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_service_servicelinkmissingst_80a5f428_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_servicelinkmissingstopwarning_stops_pkey"
        ),
        UniqueConstraint(
            "servicelinkmissingstopwarning_id",
            "stoppoint_id",
            name="data_quality_servicelink_servicelinkmissingstopwa_66ac7171_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    servicelinkmissingstopwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    stoppoint_id: Mapped[int] = mapped_column(Integer)

    servicelinkmissingstopwarning: Mapped[
        "DataQualityServicelinkmissingstopwarning"
    ] = relationship(
        "DataQualityServicelinkmissingstopwarning",
        back_populates="data_quality_servicelinkmissingstopwarning_stops",
    )


class DataQualitySlowlinkwarningServiceLinks(Base):
    __tablename__ = "data_quality_slowlinkwarning_service_links"
    __table_args__ = (
        ForeignKeyConstraint(
            ["slowlinkwarning_id"],
            ["data_quality_slowlinkwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_slowlin_slowlinkwarning_id_f6c0aa54_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_slowlinkwarning_service_links_pkey"
        ),
        UniqueConstraint(
            "slowlinkwarning_id",
            "servicelink_id",
            name="data_quality_slowlinkwar_slowlinkwarning_id_servi_8e46a2e6_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slowlinkwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    slowlinkwarning: Mapped["DataQualitySlowlinkwarning"] = relationship(
        "DataQualitySlowlinkwarning",
        back_populates="data_quality_slowlinkwarning_service_links",
    )


class DataQualitySlowlinkwarningTimings(Base):
    __tablename__ = "data_quality_slowlinkwarning_timings"
    __table_args__ = (
        ForeignKeyConstraint(
            ["slowlinkwarning_id"],
            ["data_quality_slowlinkwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_slowlin_slowlinkwarning_id_ff4aeffa_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timingpatternstop_id"],
            ["data_quality_timingpatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_slowlin_timingpatternstop_id_00b7a0e2_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_slowlinkwarning_timings_pkey"),
        UniqueConstraint(
            "slowlinkwarning_id",
            "timingpatternstop_id",
            name="data_quality_slowlinkwar_slowlinkwarning_id_timin_1ce30f09_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slowlinkwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    slowlinkwarning: Mapped["DataQualitySlowlinkwarning"] = relationship(
        "DataQualitySlowlinkwarning",
        back_populates="data_quality_slowlinkwarning_timings",
    )
    timingpatternstop: Mapped["DataQualityTimingpatternstop"] = relationship(
        "DataQualityTimingpatternstop",
        back_populates="data_quality_slowlinkwarning_timings",
    )


class DataQualitySlowtimingwarningServiceLinks(Base):
    __tablename__ = "data_quality_slowtimingwarning_service_links"
    __table_args__ = (
        ForeignKeyConstraint(
            ["slowtimingwarning_id"],
            ["data_quality_slowtimingwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_slowtim_slowtimingwarning_id_07e15f5e_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_slowtimingwarning_service_links_pkey"
        ),
        UniqueConstraint(
            "slowtimingwarning_id",
            "servicelink_id",
            name="data_quality_slowtimingw_slowtimingwarning_id_ser_56a85bc5_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slowtimingwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    slowtimingwarning: Mapped["DataQualitySlowtimingwarning"] = relationship(
        "DataQualitySlowtimingwarning",
        back_populates="data_quality_slowtimingwarning_service_links",
    )


class DataQualitySlowtimingwarningTimings(Base):
    __tablename__ = "data_quality_slowtimingwarning_timings"
    __table_args__ = (
        ForeignKeyConstraint(
            ["slowtimingwarning_id"],
            ["data_quality_slowtimingwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_slowtim_slowtimingwarning_id_b03885d1_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timingpatternstop_id"],
            ["data_quality_timingpatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_slowtim_timingpatternstop_id_c2e28015_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_slowtimingwarning_timings_pkey"),
        UniqueConstraint(
            "slowtimingwarning_id",
            "timingpatternstop_id",
            name="data_quality_slowtimingw_slowtimingwarning_id_tim_ecaed26b_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slowtimingwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    slowtimingwarning: Mapped["DataQualitySlowtimingwarning"] = relationship(
        "DataQualitySlowtimingwarning",
        back_populates="data_quality_slowtimingwarning_timings",
    )
    timingpatternstop: Mapped["DataQualityTimingpatternstop"] = relationship(
        "DataQualityTimingpatternstop",
        back_populates="data_quality_slowtimingwarning_timings",
    )


class DataQualityStopincorrecttypewarningServicePatterns(Base):
    __tablename__ = "data_quality_stopincorrecttypewarning_service_patterns"
    __table_args__ = (
        ForeignKeyConstraint(
            ["stopincorrecttypewarning_id"],
            ["data_quality_stopincorrecttypewarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_stopinc_stopincorrecttypewar_e4a4c458_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_stopincorrecttypewarning_service_patterns_pkey"
        ),
        UniqueConstraint(
            "stopincorrecttypewarning_id",
            "servicepattern_id",
            name="data_quality_stopincorre_stopincorrecttypewarning_ccd91531_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stopincorrecttypewarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicepattern_id: Mapped[int] = mapped_column(Integer)

    stopincorrecttypewarning: Mapped["DataQualityStopincorrecttypewarning"] = (
        relationship(
            "DataQualityStopincorrecttypewarning",
            back_populates="data_quality_stopincorrecttypewarning_service_patterns",
        )
    )


class DataQualityStopmissingnaptanwarningServicePatterns(Base):
    __tablename__ = "data_quality_stopmissingnaptanwarning_service_patterns"
    __table_args__ = (
        ForeignKeyConstraint(
            ["stopmissingnaptanwarning_id"],
            ["data_quality_stopmissingnaptanwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_stopmis_stopmissingnaptanwar_9932b7aa_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_stopmissingnaptanwarning_service_patterns_pkey"
        ),
        UniqueConstraint(
            "stopmissingnaptanwarning_id",
            "servicepattern_id",
            name="data_quality_stopmissing_stopmissingnaptanwarning_84937641_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stopmissingnaptanwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicepattern_id: Mapped[int] = mapped_column(Integer)

    stopmissingnaptanwarning: Mapped["DataQualityStopmissingnaptanwarning"] = (
        relationship(
            "DataQualityStopmissingnaptanwarning",
            back_populates="data_quality_stopmissingnaptanwarning_service_patterns",
        )
    )


class DataQualityTimingbackwardswarningServiceLinks(Base):
    __tablename__ = "data_quality_timingbackwardswarning_service_links"
    __table_args__ = (
        ForeignKeyConstraint(
            ["timingbackwardswarning_id"],
            ["data_quality_timingbackwardswarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingb_timingbackwardswarni_33378919_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_timingbackwardswarning_service_links_pkey"
        ),
        UniqueConstraint(
            "timingbackwardswarning_id",
            "servicelink_id",
            name="data_quality_timingbackw_timingbackwardswarning_i_e960f12c_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingbackwardswarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    timingbackwardswarning: Mapped["DataQualityTimingbackwardswarning"] = relationship(
        "DataQualityTimingbackwardswarning",
        back_populates="data_quality_timingbackwardswarning_service_links",
    )


class DataQualityTimingbackwardswarningTimings(Base):
    __tablename__ = "data_quality_timingbackwardswarning_timings"
    __table_args__ = (
        ForeignKeyConstraint(
            ["timingbackwardswarning_id"],
            ["data_quality_timingbackwardswarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingb_timingbackwardswarni_4cddfbb9_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timingpatternstop_id"],
            ["data_quality_timingpatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingb_timingpatternstop_id_dd026456_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_timingbackwardswarning_timings_pkey"
        ),
        UniqueConstraint(
            "timingbackwardswarning_id",
            "timingpatternstop_id",
            name="data_quality_timingbackw_timingbackwardswarning_i_0836746d_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingbackwardswarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    timingbackwardswarning: Mapped["DataQualityTimingbackwardswarning"] = relationship(
        "DataQualityTimingbackwardswarning",
        back_populates="data_quality_timingbackwardswarning_timings",
    )
    timingpatternstop: Mapped["DataQualityTimingpatternstop"] = relationship(
        "DataQualityTimingpatternstop",
        back_populates="data_quality_timingbackwardswarning_timings",
    )


class DataQualityTimingdropoffwarningServiceLinks(Base):
    __tablename__ = "data_quality_timingdropoffwarning_service_links"
    __table_args__ = (
        ForeignKeyConstraint(
            ["timingdropoffwarning_id"],
            ["data_quality_timingdropoffwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingd_timingdropoffwarning_c5eeefe5_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_timingdropoffwarning_service_links_pkey"
        ),
        UniqueConstraint(
            "timingdropoffwarning_id",
            "servicelink_id",
            name="data_quality_timingdropo_timingdropoffwarning_id__7703a3c2_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingdropoffwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    timingdropoffwarning: Mapped["DataQualityTimingdropoffwarning"] = relationship(
        "DataQualityTimingdropoffwarning",
        back_populates="data_quality_timingdropoffwarning_service_links",
    )


class DataQualityTimingdropoffwarningTimings(Base):
    __tablename__ = "data_quality_timingdropoffwarning_timings"
    __table_args__ = (
        ForeignKeyConstraint(
            ["timingdropoffwarning_id"],
            ["data_quality_timingdropoffwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingd_timingdropoffwarning_48fe6f3c_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timingpatternstop_id"],
            ["data_quality_timingpatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingd_timingpatternstop_id_52e080b9_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_timingdropoffwarning_timings_pkey"
        ),
        UniqueConstraint(
            "timingdropoffwarning_id",
            "timingpatternstop_id",
            name="data_quality_timingdropo_timingdropoffwarning_id__883e8f77_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingdropoffwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    timingdropoffwarning: Mapped["DataQualityTimingdropoffwarning"] = relationship(
        "DataQualityTimingdropoffwarning",
        back_populates="data_quality_timingdropoffwarning_timings",
    )
    timingpatternstop: Mapped["DataQualityTimingpatternstop"] = relationship(
        "DataQualityTimingpatternstop",
        back_populates="data_quality_timingdropoffwarning_timings",
    )


class DataQualityTimingfirstwarningServiceLinks(Base):
    __tablename__ = "data_quality_timingfirstwarning_service_links"
    __table_args__ = (
        ForeignKeyConstraint(
            ["timingfirstwarning_id"],
            ["data_quality_timingfirstwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingf_timingfirstwarning_i_3a4e8aca_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_timingfirstwarning_service_links_pkey"
        ),
        UniqueConstraint(
            "timingfirstwarning_id",
            "servicelink_id",
            name="data_quality_timingfirst_timingfirstwarning_id_se_ce4fda69_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingfirstwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    timingfirstwarning: Mapped["DataQualityTimingfirstwarning"] = relationship(
        "DataQualityTimingfirstwarning",
        back_populates="data_quality_timingfirstwarning_service_links",
    )


class DataQualityTimingfirstwarningTimings(Base):
    __tablename__ = "data_quality_timingfirstwarning_timings"
    __table_args__ = (
        ForeignKeyConstraint(
            ["timingfirstwarning_id"],
            ["data_quality_timingfirstwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingf_timingfirstwarning_i_584f81ef_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timingpatternstop_id"],
            ["data_quality_timingpatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingf_timingpatternstop_id_73681c34_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_timingfirstwarning_timings_pkey"),
        UniqueConstraint(
            "timingfirstwarning_id",
            "timingpatternstop_id",
            name="data_quality_timingfirst_timingfirstwarning_id_ti_4c2578d9_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingfirstwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    timingfirstwarning: Mapped["DataQualityTimingfirstwarning"] = relationship(
        "DataQualityTimingfirstwarning",
        back_populates="data_quality_timingfirstwarning_timings",
    )
    timingpatternstop: Mapped["DataQualityTimingpatternstop"] = relationship(
        "DataQualityTimingpatternstop",
        back_populates="data_quality_timingfirstwarning_timings",
    )


class DataQualityTiminglastwarningServiceLinks(Base):
    __tablename__ = "data_quality_timinglastwarning_service_links"
    __table_args__ = (
        ForeignKeyConstraint(
            ["timinglastwarning_id"],
            ["data_quality_timinglastwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingl_timinglastwarning_id_c66147d6_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_timinglastwarning_service_links_pkey"
        ),
        UniqueConstraint(
            "timinglastwarning_id",
            "servicelink_id",
            name="data_quality_timinglastw_timinglastwarning_id_ser_4bd4d967_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timinglastwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    timinglastwarning: Mapped["DataQualityTiminglastwarning"] = relationship(
        "DataQualityTiminglastwarning",
        back_populates="data_quality_timinglastwarning_service_links",
    )


class DataQualityTiminglastwarningTimings(Base):
    __tablename__ = "data_quality_timinglastwarning_timings"
    __table_args__ = (
        ForeignKeyConstraint(
            ["timinglastwarning_id"],
            ["data_quality_timinglastwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingl_timinglastwarning_id_9087336c_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timingpatternstop_id"],
            ["data_quality_timingpatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingl_timingpatternstop_id_e7fec441_fk_data_qual",
        ),
        PrimaryKeyConstraint("id", name="data_quality_timinglastwarning_timings_pkey"),
        UniqueConstraint(
            "timinglastwarning_id",
            "timingpatternstop_id",
            name="data_quality_timinglastw_timinglastwarning_id_tim_ba2ad23b_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timinglastwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    timinglastwarning: Mapped["DataQualityTiminglastwarning"] = relationship(
        "DataQualityTiminglastwarning",
        back_populates="data_quality_timinglastwarning_timings",
    )
    timingpatternstop: Mapped["DataQualityTimingpatternstop"] = relationship(
        "DataQualityTimingpatternstop",
        back_populates="data_quality_timinglastwarning_timings",
    )


class DataQualityTimingmissingpointwarningServiceLinks(Base):
    __tablename__ = "data_quality_timingmissingpointwarning_service_links"
    __table_args__ = (
        ForeignKeyConstraint(
            ["timingmissingpointwarning_id"],
            ["data_quality_timingmissingpointwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingm_timingmissingpointwa_cf81f506_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_timingmissingpointwarning_service_links_pkey"
        ),
        UniqueConstraint(
            "timingmissingpointwarning_id",
            "servicelink_id",
            name="data_quality_timingmissi_timingmissingpointwarnin_fa409f34_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingmissingpointwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    timingmissingpointwarning: Mapped["DataQualityTimingmissingpointwarning"] = (
        relationship(
            "DataQualityTimingmissingpointwarning",
            back_populates="data_quality_timingmissingpointwarning_service_links",
        )
    )


class DataQualityTimingmissingpointwarningTimings(Base):
    __tablename__ = "data_quality_timingmissingpointwarning_timings"
    __table_args__ = (
        ForeignKeyConstraint(
            ["timingmissingpointwarning_id"],
            ["data_quality_timingmissingpointwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingm_timingmissingpointwa_729d98d0_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timingpatternstop_id"],
            ["data_quality_timingpatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingm_timingpatternstop_id_fa1bc3cf_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_timingmissingpointwarning_timings_pkey"
        ),
        UniqueConstraint(
            "timingmissingpointwarning_id",
            "timingpatternstop_id",
            name="data_quality_timingmissi_timingmissingpointwarnin_74ac2338_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingmissingpointwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    timingmissingpointwarning: Mapped["DataQualityTimingmissingpointwarning"] = (
        relationship(
            "DataQualityTimingmissingpointwarning",
            back_populates="data_quality_timingmissingpointwarning_timings",
        )
    )
    timingpatternstop: Mapped["DataQualityTimingpatternstop"] = relationship(
        "DataQualityTimingpatternstop",
        back_populates="data_quality_timingmissingpointwarning_timings",
    )


class DataQualityTimingmultiplewarningTimings(Base):
    __tablename__ = "data_quality_timingmultiplewarning_timings"
    __table_args__ = (
        ForeignKeyConstraint(
            ["timingmultiplewarning_id"],
            ["data_quality_timingmultiplewarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingm_timingmultiplewarnin_5ad29f1d_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timingpatternstop_id"],
            ["data_quality_timingpatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingm_timingpatternstop_id_29b9b490_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_timingmultiplewarning_timings_pkey"
        ),
        UniqueConstraint(
            "timingmultiplewarning_id",
            "timingpatternstop_id",
            name="data_quality_timingmulti_timingmultiplewarning_id_5948d116_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingmultiplewarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    timingmultiplewarning: Mapped["DataQualityTimingmultiplewarning"] = relationship(
        "DataQualityTimingmultiplewarning",
        back_populates="data_quality_timingmultiplewarning_timings",
    )
    timingpatternstop: Mapped["DataQualityTimingpatternstop"] = relationship(
        "DataQualityTimingpatternstop",
        back_populates="data_quality_timingmultiplewarning_timings",
    )


class DataQualityTimingpickupwarningServiceLinks(Base):
    __tablename__ = "data_quality_timingpickupwarning_service_links"
    __table_args__ = (
        ForeignKeyConstraint(
            ["timingpickupwarning_id"],
            ["data_quality_timingpickupwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingp_timingpickupwarning__e565b9de_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_timingpickupwarning_service_links_pkey"
        ),
        UniqueConstraint(
            "timingpickupwarning_id",
            "servicelink_id",
            name="data_quality_timingpicku_timingpickupwarning_id_s_e32a5380_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingpickupwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    servicelink_id: Mapped[int] = mapped_column(Integer)

    timingpickupwarning: Mapped["DataQualityTimingpickupwarning"] = relationship(
        "DataQualityTimingpickupwarning",
        back_populates="data_quality_timingpickupwarning_service_links",
    )


class DataQualityTimingpickupwarningTimings(Base):
    __tablename__ = "data_quality_timingpickupwarning_timings"
    __table_args__ = (
        ForeignKeyConstraint(
            ["timingpatternstop_id"],
            ["data_quality_timingpatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingp_timingpatternstop_id_f18bb7fd_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["timingpickupwarning_id"],
            ["data_quality_timingpickupwarning.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_timingp_timingpickupwarning__35b76ba0_fk_data_qual",
        ),
        PrimaryKeyConstraint(
            "id", name="data_quality_timingpickupwarning_timings_pkey"
        ),
        UniqueConstraint(
            "timingpickupwarning_id",
            "timingpatternstop_id",
            name="data_quality_timingpicku_timingpickupwarning_id_t_e1f7446d_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timingpickupwarning_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    timingpatternstop_id: Mapped[int] = mapped_column(Integer)

    timingpatternstop: Mapped["DataQualityTimingpatternstop"] = relationship(
        "DataQualityTimingpatternstop",
        back_populates="data_quality_timingpickupwarning_timings",
    )
    timingpickupwarning: Mapped["DataQualityTimingpickupwarning"] = relationship(
        "DataQualityTimingpickupwarning",
        back_populates="data_quality_timingpickupwarning_timings",
    )


class FaresDatacataloguemetadata(Base):
    __tablename__ = "fares_datacataloguemetadata"
    __table_args__ = (
        ForeignKeyConstraint(
            ["fares_metadata_id"],
            ["fares_faresmetadata.datasetmetadata_ptr_id"],
            deferrable=True,
            initially="DEFERRED",
            name="fares_datacataloguem_fares_metadata_id_ca9c51db_fk_fares_far",
        ),
        PrimaryKeyConstraint("id", name="fares_datacataloguemetadata_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    xml_file_name: Mapped[str] = mapped_column(String(255))
    fares_metadata_id: Mapped[int] = mapped_column(Integer)
    valid_from: Mapped[Optional[datetime.date]] = mapped_column(Date)
    valid_to: Mapped[Optional[datetime.date]] = mapped_column(Date)
    national_operator_code: Mapped[Optional[list]] = mapped_column(
        ARRAY(String(length=255))
    )
    line_id: Mapped[Optional[list]] = mapped_column(ARRAY(String(length=100)))
    line_name: Mapped[Optional[list]] = mapped_column(ARRAY(String(length=100)))
    atco_area: Mapped[Optional[list]] = mapped_column(ARRAY(Integer()))
    tariff_basis: Mapped[Optional[list]] = mapped_column(ARRAY(String(length=100)))
    product_type: Mapped[Optional[list]] = mapped_column(ARRAY(String(length=100)))
    product_name: Mapped[Optional[list]] = mapped_column(ARRAY(String(length=100)))
    user_type: Mapped[Optional[list]] = mapped_column(ARRAY(String(length=100)))

    fares_metadata: Mapped["FaresFaresmetadata"] = relationship(
        "FaresFaresmetadata", back_populates="fares_datacataloguemetadata"
    )


class FaresFaresmetadataStops(Base):
    __tablename__ = "fares_faresmetadata_stops"
    __table_args__ = (
        ForeignKeyConstraint(
            ["faresmetadata_id"],
            ["fares_faresmetadata.datasetmetadata_ptr_id"],
            deferrable=True,
            initially="DEFERRED",
            name="fares_faresmetadata__faresmetadata_id_1fb18c75_fk_fares_far",
        ),
        PrimaryKeyConstraint("id", name="fares_faresmetadata_stops_pkey"),
        UniqueConstraint(
            "faresmetadata_id",
            "stoppoint_id",
            name="fares_faresmetadata_stop_faresmetadata_id_stoppoi_fc565357_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    faresmetadata_id: Mapped[int] = mapped_column(Integer)
    stoppoint_id: Mapped[int] = mapped_column(Integer)

    faresmetadata: Mapped["FaresFaresmetadata"] = relationship(
        "FaresFaresmetadata", back_populates="fares_faresmetadata_stops"
    )


class NaptanStoppoint(Base):
    __tablename__ = "naptan_stoppoint"
    __table_args__ = (
        ForeignKeyConstraint(
            ["admin_area_id"],
            ["naptan_adminarea.id"],
            deferrable=True,
            initially="DEFERRED",
            name="naptan_stoppoint_admin_area_id_6ccac623_fk_naptan_adminarea_id",
        ),
        ForeignKeyConstraint(
            ["locality_id"],
            ["naptan_locality.gazetteer_id"],
            deferrable=True,
            initially="DEFERRED",
            name="naptan_stoppoint_locality_id_4ef6e016_fk_naptan_lo",
        ),
        PrimaryKeyConstraint("id", name="naptan_stoppoint_pkey"),
        UniqueConstraint("atco_code", name="naptan_stoppoint_atco_code_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    atco_code: Mapped[str] = mapped_column(String(255))
    common_name: Mapped[str] = mapped_column(String(255))
    location: Mapped[Any] = mapped_column(
        Geometry(
            "POINT", 4326, from_text="ST_GeomFromEWKT", name="geometry", nullable=False
        )
    )
    stop_areas: Mapped[list] = mapped_column(ARRAY(String(length=255)))
    naptan_code: Mapped[Optional[str]] = mapped_column(String(12))
    street: Mapped[Optional[str]] = mapped_column(String(255))
    indicator: Mapped[Optional[str]] = mapped_column(String(255))
    admin_area_id: Mapped[Optional[int]] = mapped_column(Integer)
    locality_id: Mapped[Optional[str]] = mapped_column(String(8))
    bus_stop_type: Mapped[Optional[str]] = mapped_column(String(255))
    stop_type: Mapped[Optional[str]] = mapped_column(String(255))

    admin_area: Mapped[Optional["NaptanAdminarea"]] = relationship(
        "NaptanAdminarea", back_populates="naptan_stoppoint"
    )
    locality: Mapped[Optional["NaptanLocality"]] = relationship(
        "NaptanLocality", back_populates="naptan_stoppoint"
    )
    naptan_flexiblezone: Mapped[List["NaptanFlexiblezone"]] = relationship(
        "NaptanFlexiblezone", back_populates="naptan_stoppoint"
    )


class OrganisationDatasetrevisionLocalities(Base):
    __tablename__ = "organisation_datasetrevision_localities"
    __table_args__ = (
        ForeignKeyConstraint(
            ["datasetrevision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_dataset_datasetrevision_id_c2e12fc6_fk_organisat",
        ),
        ForeignKeyConstraint(
            ["locality_id"],
            ["naptan_locality.gazetteer_id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_dataset_locality_id_279c668f_fk_naptan_lo",
        ),
        PrimaryKeyConstraint("id", name="organisation_datasetrevision_localities_pkey"),
        UniqueConstraint(
            "datasetrevision_id",
            "locality_id",
            name="organisation_datasetrevi_datasetrevision_id_local_04095647_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    datasetrevision_id: Mapped[int] = mapped_column(Integer)
    locality_id: Mapped[str] = mapped_column(String(8))

    datasetrevision: Mapped["OrganisationDatasetrevision"] = relationship(
        "OrganisationDatasetrevision",
        back_populates="organisation_datasetrevision_localities",
    )
    locality: Mapped["NaptanLocality"] = relationship(
        "NaptanLocality", back_populates="organisation_datasetrevision_localities"
    )


class OrganisationSeasonalservice(Base):
    __tablename__ = "organisation_seasonalservice"
    __table_args__ = (
        ForeignKeyConstraint(
            ["licence_id"],
            ["organisation_licence.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_seasona_licence_id_bdda88fe_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="organisation_seasonalservice_pkey"),
        UniqueConstraint("licence_id", "registration_code", name="unique_service"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    registration_code: Mapped[int] = mapped_column(Integer)
    start: Mapped[datetime.date] = mapped_column(Date)
    end: Mapped[datetime.date] = mapped_column(Date)
    licence_id: Mapped[int] = mapped_column(Integer)

    licence: Mapped["OrganisationLicence"] = relationship(
        "OrganisationLicence", back_populates="organisation_seasonalservice"
    )


class OrganisationServicecodeexemption(Base):
    __tablename__ = "organisation_servicecodeexemption"
    __table_args__ = (
        ForeignKeyConstraint(
            ["exempted_by_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_service_exempted_by_id_6b2e4915_fk_users_use",
        ),
        ForeignKeyConstraint(
            ["licence_id"],
            ["organisation_licence.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_service_licence_id_0dd3ef97_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="organisation_servicecodeexemption_pkey"),
        UniqueConstraint(
            "licence_id",
            "registration_code",
            name="organisation_servicecode_licence_id_registration__c5755fe0_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    registration_code: Mapped[str] = mapped_column(String(50))
    justification: Mapped[str] = mapped_column(String(140))
    exempted_by_id: Mapped[int] = mapped_column(Integer)
    licence_id: Mapped[int] = mapped_column(Integer)

    exempted_by: Mapped["UsersUser"] = relationship(
        "UsersUser", back_populates="organisation_servicecodeexemption"
    )
    licence: Mapped["OrganisationLicence"] = relationship(
        "OrganisationLicence", back_populates="organisation_servicecodeexemption"
    )


class TransmodelBookingarrangements(Base):
    __tablename__ = "transmodel_bookingarrangements"
    __table_args__ = (
        CheckConstraint(
            "email IS NOT NULL AND NOT (email::text = ''::text AND email IS NOT NULL) OR phone_number IS NOT NULL AND NOT (phone_number::text = ''::text AND phone_number IS NOT NULL) OR web_address IS NOT NULL AND NOT (web_address::text = ''::text AND web_address IS NOT NULL)",
            name="at_least_one_column_not_empty_or_null",
        ),
        ForeignKeyConstraint(
            ["service_id"],
            ["transmodel_service.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_bookingar_service_id_967a65d6_fk_transmode",
        ),
        PrimaryKeyConstraint("id", name="transmodel_bookingarrangements_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    service_id: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[Optional[str]] = mapped_column(String(254))
    phone_number: Mapped[Optional[str]] = mapped_column(String(16))
    web_address: Mapped[Optional[str]] = mapped_column(String(200))

    service: Mapped["TransmodelService"] = relationship(
        "TransmodelService", back_populates="transmodel_bookingarrangements"
    )


class TransmodelFlexibleserviceoperationperiod(Base):
    __tablename__ = "transmodel_flexibleserviceoperationperiod"
    __table_args__ = (
        ForeignKeyConstraint(
            ["vehicle_journey_id"],
            ["transmodel_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_flexibles_vehicle_journey_id_e3d1299e_fk_transmode",
        ),
        PrimaryKeyConstraint(
            "id", name="transmodel_flexibleserviceoperationperiod_pkey"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)
    end_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    start_time: Mapped[Optional[datetime.time]] = mapped_column(Time)

    vehicle_journey: Mapped["TransmodelVehiclejourney"] = relationship(
        "TransmodelVehiclejourney",
        back_populates="transmodel_flexibleserviceoperationperiod",
    )


class TransmodelNonoperatingdatesexceptions(Base):
    __tablename__ = "transmodel_nonoperatingdatesexceptions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["vehicle_journey_id"],
            ["transmodel_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_nonoperat_vehicle_journey_id_f3d4bc65_fk_transmode",
        ),
        PrimaryKeyConstraint("id", name="transmodel_nonoperatingdatesexceptions_pkey"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)
    non_operating_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    vehicle_journey: Mapped["TransmodelVehiclejourney"] = relationship(
        "TransmodelVehiclejourney",
        back_populates="transmodel_nonoperatingdatesexceptions",
    )


class TransmodelOperatingdatesexceptions(Base):
    __tablename__ = "transmodel_operatingdatesexceptions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["vehicle_journey_id"],
            ["transmodel_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_operating_vehicle_journey_id_7df49157_fk_transmode",
        ),
        PrimaryKeyConstraint("id", name="transmodel_operatingdatesexceptions_pkey"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)
    operating_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    vehicle_journey: Mapped["TransmodelVehiclejourney"] = relationship(
        "TransmodelVehiclejourney", back_populates="transmodel_operatingdatesexceptions"
    )


class TransmodelOperatingprofile(Base):
    __tablename__ = "transmodel_operatingprofile"
    __table_args__ = (
        ForeignKeyConstraint(
            ["vehicle_journey_id"],
            ["transmodel_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_operating_vehicle_journey_id_64fb5bad_fk_transmode",
        ),
        PrimaryKeyConstraint("id", name="transmodel_operatingprofile_pkey"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    day_of_week: Mapped[str] = mapped_column(String(20))
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)

    vehicle_journey: Mapped["TransmodelVehiclejourney"] = relationship(
        "TransmodelVehiclejourney", back_populates="transmodel_operatingprofile"
    )


class TransmodelServiceServicePatterns(Base):
    __tablename__ = "transmodel_service_service_patterns"
    __table_args__ = (
        ForeignKeyConstraint(
            ["service_id"],
            ["transmodel_service.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_service_s_service_id_6fae3b23_fk_transmode",
        ),
        PrimaryKeyConstraint("id", name="transmodel_service_service_patterns_pkey"),
        UniqueConstraint(
            "service_id",
            "servicepattern_id",
            name="transmodel_service_servi_service_id_servicepatter_8d00b2d4_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_id: Mapped[int] = mapped_column(Integer)
    servicepattern_id: Mapped[int] = mapped_column(Integer)

    service: Mapped["TransmodelService"] = relationship(
        "TransmodelService", back_populates="transmodel_service_service_patterns"
    )


class TransmodelServicedorganisationvehiclejourney(Base):
    __tablename__ = "transmodel_servicedorganisationvehiclejourney"
    __table_args__ = (
        ForeignKeyConstraint(
            ["serviced_organisation_id"],
            ["transmodel_servicedorganisations.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_servicedo_serviced_organisatio_4f5b7f54_fk_transmode",
        ),
        ForeignKeyConstraint(
            ["vehicle_journey_id"],
            ["transmodel_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_servicedo_vehicle_journey_id_da3adc3a_fk_transmode",
        ),
        PrimaryKeyConstraint(
            "id", name="transmodel_servicedorganisationvehiclejourney_pkey"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    operating_on_working_days: Mapped[bool] = mapped_column(Boolean)
    serviced_organisation_id: Mapped[int] = mapped_column(Integer)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)

    serviced_organisation: Mapped["TransmodelServicedorganisations"] = relationship(
        "TransmodelServicedorganisations",
        back_populates="transmodel_servicedorganisationvehiclejourney",
    )
    vehicle_journey: Mapped["TransmodelVehiclejourney"] = relationship(
        "TransmodelVehiclejourney",
        back_populates="transmodel_servicedorganisationvehiclejourney",
    )
    dqs_observationresults: Mapped[List["DqsObservationresults"]] = relationship(
        "DqsObservationresults", back_populates="serviced_organisation_vehicle_journey"
    )
    transmodel_servicedorganisationworkingdays: Mapped[
        List["TransmodelServicedorganisationworkingdays"]
    ] = relationship(
        "TransmodelServicedorganisationworkingdays",
        back_populates="serviced_organisation_vehicle_journey",
    )


class TransmodelServicepatternLocalities(Base):
    __tablename__ = "transmodel_servicepattern_localities"
    __table_args__ = (
        ForeignKeyConstraint(
            ["locality_id"],
            ["naptan_locality.gazetteer_id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_servicepa_locality_id_8333c340_fk_naptan_lo",
        ),
        PrimaryKeyConstraint("id", name="transmodel_servicepattern_localities_pkey"),
        UniqueConstraint(
            "servicepattern_id",
            "locality_id",
            name="transmodel_servicepatter_servicepattern_id_locali_9b3532e4_uniq",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    servicepattern_id: Mapped[int] = mapped_column(Integer)
    locality_id: Mapped[str] = mapped_column(String(8))

    locality: Mapped["NaptanLocality"] = relationship(
        "NaptanLocality", back_populates="transmodel_servicepattern_localities"
    )


class TransmodelServicepatternstop(Base):
    __tablename__ = "transmodel_servicepatternstop"
    __table_args__ = (
        ForeignKeyConstraint(
            ["stop_activity_id"],
            ["transmodel_stopactivity.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_servicepa_stop_activity_id_cd96c52d_fk_transmode",
        ),
        ForeignKeyConstraint(
            ["vehicle_journey_id"],
            ["transmodel_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_servicepa_vehicle_journey_id_32f3f1c9_fk_transmode",
        ),
        PrimaryKeyConstraint("id", name="transmodel_servicepatternstop_pkey"),
    )

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

    stop_activity: Mapped[Optional["TransmodelStopactivity"]] = relationship(
        "TransmodelStopactivity", back_populates="transmodel_servicepatternstop"
    )
    vehicle_journey: Mapped[Optional["TransmodelVehiclejourney"]] = relationship(
        "TransmodelVehiclejourney", back_populates="transmodel_servicepatternstop"
    )
    data_quality_observationresults: Mapped[List["DataQualityObservationresults"]] = (
        relationship(
            "DataQualityObservationresults", back_populates="service_pattern_stop"
        )
    )
    dqs_observationresults: Mapped[List["DqsObservationresults"]] = relationship(
        "DqsObservationresults", back_populates="service_pattern_stop"
    )
    organisation_consumerfeedback: Mapped[List["OrganisationConsumerfeedback"]] = (
        relationship(
            "OrganisationConsumerfeedback", back_populates="service_pattern_stop"
        )
    )


class TransmodelTracksvehiclejourney(Base):
    __tablename__ = "transmodel_tracksvehiclejourney"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tracks_id"],
            ["transmodel_tracks.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_tracksveh_tracks_id_dfff07ad_fk_transmode",
        ),
        ForeignKeyConstraint(
            ["vehicle_journey_id"],
            ["transmodel_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_tracksveh_vehicle_journey_id_15910233_fk_transmode",
        ),
        PrimaryKeyConstraint("id", name="transmodel_tracksvehiclejourney_pkey"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    tracks_id: Mapped[int] = mapped_column(Integer)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)
    sequence_number: Mapped[Optional[int]] = mapped_column(Integer)

    tracks: Mapped["TransmodelTracks"] = relationship(
        "TransmodelTracks", back_populates="transmodel_tracksvehiclejourney"
    )
    vehicle_journey: Mapped["TransmodelVehiclejourney"] = relationship(
        "TransmodelVehiclejourney", back_populates="transmodel_tracksvehiclejourney"
    )


class UsersAgentuserinvite(Base):
    __tablename__ = "users_agentuserinvite"
    __table_args__ = (
        ForeignKeyConstraint(
            ["agent_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="users_agentuserinvite_agent_id_7f289298_fk_users_user_id",
        ),
        ForeignKeyConstraint(
            ["invitation_id"],
            ["users_invitation.invitation_ptr_id"],
            deferrable=True,
            initially="DEFERRED",
            name="users_agentuserinvite_invitation_id_9a4f7a14_fk",
        ),
        ForeignKeyConstraint(
            ["inviter_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="users_agentuserinvite_inviter_id_c58edfec_fk_users_user_id",
        ),
        ForeignKeyConstraint(
            ["organisation_id"],
            ["organisation_organisation.id"],
            deferrable=True,
            initially="DEFERRED",
            name="users_agentuserinvit_organisation_id_ef4219bf_fk_organisat",
        ),
        PrimaryKeyConstraint("id", name="users_agentuserinvite_pkey"),
        UniqueConstraint(
            "invitation_id", name="users_agentuserinvite_invitation_id_key"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String(50))
    inviter_id: Mapped[int] = mapped_column(Integer)
    organisation_id: Mapped[int] = mapped_column(Integer)
    agent_id: Mapped[Optional[int]] = mapped_column(Integer)
    invitation_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    agent: Mapped[Optional["UsersUser"]] = relationship(
        "UsersUser", foreign_keys=[agent_id], back_populates="users_agentuserinvite"
    )
    invitation: Mapped[Optional["UsersInvitation"]] = relationship(
        "UsersInvitation", back_populates="users_agentuserinvite"
    )
    inviter: Mapped["UsersUser"] = relationship(
        "UsersUser", foreign_keys=[inviter_id], back_populates="users_agentuserinvite_"
    )
    organisation: Mapped["OrganisationOrganisation"] = relationship(
        "OrganisationOrganisation", back_populates="users_agentuserinvite"
    )


class DataQualityObservationresults(Base):
    __tablename__ = "data_quality_observationresults"
    __table_args__ = (
        ForeignKeyConstraint(
            ["service_pattern_stop_id"],
            ["transmodel_servicepatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_observa_service_pattern_stop_acfb59f8_fk_transmode",
        ),
        ForeignKeyConstraint(
            ["taskresults_id"],
            ["data_quality_taskresults.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_observa_taskresults_id_bef2bc9b_fk_data_qual",
        ),
        ForeignKeyConstraint(
            ["vehicle_journey_id"],
            ["transmodel_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="data_quality_observa_vehicle_journey_id_56675539_fk_transmode",
        ),
        PrimaryKeyConstraint("id", name="data_quality_observationresults_pkey"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    details: Mapped[str] = mapped_column(Text)
    service_pattern_stop_id: Mapped[int] = mapped_column(Integer)
    taskresults_id: Mapped[int] = mapped_column(Integer)
    vehicle_journey_id: Mapped[int] = mapped_column(Integer)

    service_pattern_stop: Mapped["TransmodelServicepatternstop"] = relationship(
        "TransmodelServicepatternstop", back_populates="data_quality_observationresults"
    )
    taskresults: Mapped["DataQualityTaskresults"] = relationship(
        "DataQualityTaskresults", back_populates="data_quality_observationresults"
    )
    vehicle_journey: Mapped["TransmodelVehiclejourney"] = relationship(
        "TransmodelVehiclejourney", back_populates="data_quality_observationresults"
    )


class DqsObservationresults(Base):
    __tablename__ = "dqs_observationresults"
    __table_args__ = (
        ForeignKeyConstraint(
            ["service_pattern_stop_id"],
            ["transmodel_servicepatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="dqs_observationresults_service_pattern_stop_id_603d0be8_fk",
        ),
        ForeignKeyConstraint(
            ["serviced_organisation_vehicle_journey_id"],
            ["transmodel_servicedorganisationvehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="dqs_observationresul_serviced_organisatio_b564ba8e_fk_transmode",
        ),
        ForeignKeyConstraint(
            ["taskresults_id"],
            ["dqs_taskresults.id"],
            deferrable=True,
            initially="DEFERRED",
            name="dqs_observationresul_taskresults_id_80858afc_fk_dqs_taskr",
        ),
        ForeignKeyConstraint(
            ["vehicle_journey_id"],
            ["transmodel_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="dqs_observationresul_vehicle_journey_id_6e76a0f9_fk_transmode",
        ),
        PrimaryKeyConstraint("id", name="dqs_observationresults_pkey"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    details: Mapped[str] = mapped_column(Text)
    taskresults_id: Mapped[int] = mapped_column(Integer)
    service_pattern_stop_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    vehicle_journey_id: Mapped[Optional[int]] = mapped_column(Integer)
    is_suppressed: Mapped[Optional[bool]] = mapped_column(Boolean)
    serviced_organisation_vehicle_journey_id: Mapped[Optional[int]] = mapped_column(
        Integer
    )

    service_pattern_stop: Mapped[Optional["TransmodelServicepatternstop"]] = (
        relationship(
            "TransmodelServicepatternstop", back_populates="dqs_observationresults"
        )
    )
    serviced_organisation_vehicle_journey: Mapped[
        Optional["TransmodelServicedorganisationvehiclejourney"]
    ] = relationship(
        "TransmodelServicedorganisationvehiclejourney",
        back_populates="dqs_observationresults",
    )
    taskresults: Mapped["DqsTaskresults"] = relationship(
        "DqsTaskresults", back_populates="dqs_observationresults"
    )
    vehicle_journey: Mapped[Optional["TransmodelVehiclejourney"]] = relationship(
        "TransmodelVehiclejourney", back_populates="dqs_observationresults"
    )


class NaptanFlexiblezone(Base):
    __tablename__ = "naptan_flexiblezone"
    __table_args__ = (
        ForeignKeyConstraint(
            ["naptan_stoppoint_id"],
            ["naptan_stoppoint.id"],
            deferrable=True,
            initially="DEFERRED",
            name="naptan_flexiblezone_naptan_stoppoint_id_d2845c0f_fk_naptan_st",
        ),
        PrimaryKeyConstraint("id", name="naptan_flexiblezone_pkey"),
        UniqueConstraint(
            "naptan_stoppoint_id", "sequence_number", name="unique_flexible_zone"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    sequence_number: Mapped[int] = mapped_column(Integer)
    location: Mapped[Any] = mapped_column(
        Geometry(
            "POINT", 4326, from_text="ST_GeomFromEWKT", name="geometry", nullable=False
        )
    )
    naptan_stoppoint_id: Mapped[int] = mapped_column(Integer)

    naptan_stoppoint: Mapped["NaptanStoppoint"] = relationship(
        "NaptanStoppoint", back_populates="naptan_flexiblezone"
    )


class OrganisationConsumerfeedback(Base):
    __tablename__ = "organisation_consumerfeedback"
    __table_args__ = (
        ForeignKeyConstraint(
            ["consumer_id"],
            ["users_user.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_consume_consumer_id_ca3311e6_fk_users_use",
        ),
        ForeignKeyConstraint(
            ["dataset_id"],
            ["organisation_dataset.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_consume_dataset_id_8294a373_fk_organisat",
        ),
        ForeignKeyConstraint(
            ["organisation_id"],
            ["organisation_organisation.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_consume_organisation_id_a67e8216_fk_organisat",
        ),
        ForeignKeyConstraint(
            ["revision_id"],
            ["organisation_datasetrevision.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_consume_revision_id_dfaf8ec8_fk_organisat",
        ),
        ForeignKeyConstraint(
            ["service_id"],
            ["transmodel_service.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_consume_service_id_9f942cd4_fk_transmode",
        ),
        ForeignKeyConstraint(
            ["service_pattern_id"],
            ["transmodel_servicepattern.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_consume_service_pattern_id_b1625f30_fk_transmode",
        ),
        ForeignKeyConstraint(
            ["service_pattern_stop_id"],
            ["transmodel_servicepatternstop.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_consume_service_pattern_stop_b0db9428_fk_transmode",
        ),
        ForeignKeyConstraint(
            ["vehicle_journey_id"],
            ["transmodel_vehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="organisation_consume_vehicle_journey_id_ae0d3c6b_fk_transmode",
        ),
        PrimaryKeyConstraint("id", name="organisation_consumerfeedback_pkey"),
    )

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

    consumer: Mapped[Optional["UsersUser"]] = relationship(
        "UsersUser", back_populates="organisation_consumerfeedback"
    )
    dataset: Mapped[Optional["OrganisationDataset"]] = relationship(
        "OrganisationDataset", back_populates="organisation_consumerfeedback"
    )
    organisation: Mapped["OrganisationOrganisation"] = relationship(
        "OrganisationOrganisation", back_populates="organisation_consumerfeedback"
    )
    revision: Mapped[Optional["OrganisationDatasetrevision"]] = relationship(
        "OrganisationDatasetrevision", back_populates="organisation_consumerfeedback"
    )
    service: Mapped[Optional["TransmodelService"]] = relationship(
        "TransmodelService", back_populates="organisation_consumerfeedback"
    )
    service_pattern: Mapped[Optional["TransmodelServicepattern"]] = relationship(
        "TransmodelServicepattern", back_populates="organisation_consumerfeedback"
    )
    service_pattern_stop: Mapped[Optional["TransmodelServicepatternstop"]] = (
        relationship(
            "TransmodelServicepatternstop",
            back_populates="organisation_consumerfeedback",
        )
    )
    vehicle_journey: Mapped[Optional["TransmodelVehiclejourney"]] = relationship(
        "TransmodelVehiclejourney", back_populates="organisation_consumerfeedback"
    )


class TransmodelServicedorganisationworkingdays(Base):
    __tablename__ = "transmodel_servicedorganisationworkingdays"
    __table_args__ = (
        ForeignKeyConstraint(
            ["serviced_organisation_vehicle_journey_id"],
            ["transmodel_servicedorganisationvehiclejourney.id"],
            deferrable=True,
            initially="DEFERRED",
            name="transmodel_servicedo_serviced_organisatio_f3dc5685_fk_transmode",
        ),
        PrimaryKeyConstraint(
            "id", name="transmodel_servicedorganisationworkingdays_pkey"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    start_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    serviced_organisation_vehicle_journey_id: Mapped[Optional[int]] = mapped_column(
        Integer
    )

    serviced_organisation_vehicle_journey: Mapped[
        Optional["TransmodelServicedorganisationvehiclejourney"]
    ] = relationship(
        "TransmodelServicedorganisationvehiclejourney",
        back_populates="transmodel_servicedorganisationworkingdays",
    )
