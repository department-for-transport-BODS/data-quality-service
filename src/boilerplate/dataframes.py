from common import Check, DQSReport
import pandas as pd
import geoalchemy2
from sqlalchemy.sql.functions import coalesce
from typing import List
from sqlalchemy import and_, select, asc, desc


def get_df_vehicle_journey(check: Check) -> pd.DataFrame:
    """
    Get the dataframe containing the vehicle journey and the stop activity

    """

    Service = check.db.classes.transmodel_service
    ServicePatternService = check.db.classes.transmodel_service_service_patterns
    ServicePatternStop = check.db.classes.transmodel_servicepatternstop
    StopActivity = check.db.classes.transmodel_stopactivity
    VehicleJourney = check.db.classes.transmodel_vehiclejourney
    NaptanStopPoint = check.db.classes.naptan_stoppoint

    result = (
        check.db.session.query(Service)
        .join(ServicePatternService, Service.id == ServicePatternService.service_id)
        .join(
            ServicePatternStop,
            ServicePatternService.servicepattern_id
            == ServicePatternStop.service_pattern_id,
        )
        .join(StopActivity, ServicePatternStop.stop_activity_id == StopActivity.id)
        .join(
            VehicleJourney, ServicePatternStop.vehicle_journey_id == VehicleJourney.id
        )
        .join(
            NaptanStopPoint,
            ServicePatternStop.naptan_stop_id == NaptanStopPoint.id,
            isouter=True,
        )
        .where(Service.txcfileattributes_id == check.file_id)
        .with_entities(
            ServicePatternStop.is_timing_point.label("is_timing_point"),
            ServicePatternStop.naptan_stop_id.label("naptan_stop_id"),
            ServicePatternStop.auto_sequence_number.label("auto_sequence_number"),
            ServicePatternStop.atco_code.label("atco_code"),
            ServicePatternStop.departure_time.label("departure_time"),
            coalesce(
                NaptanStopPoint.common_name, ServicePatternStop.txc_common_name
            ).label("common_name"),
            ServicePatternStop.id.label("service_pattern_stop_id"),
            StopActivity.name.label("activity"),
            VehicleJourney.start_time.label("start_time"),
            VehicleJourney.direction.label("direction"),
            VehicleJourney.id.label("vehicle_journey_id"),
        )
    )
    return pd.read_sql_query(result.statement, check.db.session.bind)


def get_df_stop_type(check: Check, allowed_stop_types: List) -> pd.DataFrame:
    """
    Get the dataframe containing the vehicle journey and the stop type

    """

    Service = check.db.classes.transmodel_service
    ServicePatternService = check.db.classes.transmodel_service_service_patterns
    ServicePatternStop = check.db.classes.transmodel_servicepatternstop
    VehicleJourney = check.db.classes.transmodel_vehiclejourney
    NaptanStopPoint = check.db.classes.naptan_stoppoint

    columns = [
        "atco_code",
        "service_pattern_stop_id",
        "common_name",
        "vehicle_journey_id",
        "stop_type",
    ]

    result = (
        check.db.session.query(Service)
        .join(ServicePatternService, Service.id == ServicePatternService.service_id)
        .join(
            ServicePatternStop,
            ServicePatternService.servicepattern_id
            == ServicePatternStop.service_pattern_id,
        )
        .join(
            VehicleJourney, ServicePatternStop.vehicle_journey_id == VehicleJourney.id
        )
        .join(NaptanStopPoint, ServicePatternStop.naptan_stop_id == NaptanStopPoint.id)
        .where(
            and_(
                ~NaptanStopPoint.stop_type.in_(allowed_stop_types),
                Service.txcfileattributes_id == check.file_id,
            )
        )
        .with_entities(
            ServicePatternStop.atco_code,
            ServicePatternStop.id,
            coalesce(NaptanStopPoint.common_name, ServicePatternStop.txc_common_name),
            VehicleJourney.id,
            NaptanStopPoint.stop_type,
        )
    )

    result = result.all()

    return pd.DataFrame.from_records(result, columns=columns)


def get_df_dqs_observation_results(report: DQSReport) -> pd.DataFrame:
    """
    Get the dataframe with observation results
    """
    dqs_observationresults = report.db.classes.dqs_observationresults
    dqs_taskresults = report.db.classes.dqs_taskresults
    dqs_report = report.db.classes.dqs_report
    dqs_checks = report.db.classes.dqs_checks
    organisation_txcfileattributes = report.db.classes.organisation_txcfileattributes
    transmodel_service = report.db.classes.transmodel_service

    result = (
        report.db.session.query(
            dqs_checks.importance.label("Importance"),
            dqs_checks.category.label("Category"),
            dqs_checks.observation.label("Observation"),
            transmodel_service.service_code.label("Registration Number"),
            transmodel_service.name.label("Service"),
            dqs_observationresults.details.label("Details")
        )
        .join(dqs_taskresults, dqs_observationresults.taskresults_id == dqs_taskresults.id)
        .join(dqs_report, dqs_taskresults.dataquality_report_id == dqs_report.id)
        .join(dqs_checks, dqs_taskresults.checks_id == dqs_checks.id)
        .join(organisation_txcfileattributes, organisation_txcfileattributes.id == dqs_taskresults.transmodel_txcfileattributes_id)
        .join(transmodel_service, transmodel_service.txcfileattributes_id == organisation_txcfileattributes.id)
        .filter(dqs_report.id == report.report_id)
    )

    return pd.read_sql_query(result.statement, report.db.session.bind)


def get_vj_duplicate_journey_code(check: Check) -> pd.DataFrame:
    """
    Get the dataframe containing the vehicle journey and stop point
    including operating profile, non operating dates, operating dates
    and serviced organisation
    """
    VehicleJourney = check.db.classes.transmodel_vehiclejourney
    OperatingProfile = check.db.classes.transmodel_operatingprofile
    OperatingDatesExceptions = check.db.classes.transmodel_operatingdatesexceptions
    NonOperatingdatesexceptions = (
        check.db.classes.transmodel_nonoperatingdatesexceptions
    )
    ServicedOrganisationVehicleJourney = (
        check.db.classes.transmodel_servicedorganisationvehiclejourney
    )

    Service = check.db.classes.transmodel_service
    ServicePatternService = check.db.classes.transmodel_service_service_patterns
    ServicePatternStop = check.db.classes.transmodel_servicepatternstop

    result = (
        check.db.session.query(Service)
        .join(ServicePatternService, Service.id == ServicePatternService.service_id)
        .join(
            ServicePatternStop,
            ServicePatternService.servicepattern_id
            == ServicePatternStop.service_pattern_id,
        )
        .join(
            VehicleJourney, ServicePatternStop.vehicle_journey_id == VehicleJourney.id
        )
        .outerjoin(
            OperatingProfile, VehicleJourney.id == OperatingProfile.vehicle_journey_id
        )
        .outerjoin(
            OperatingDatesExceptions,
            VehicleJourney.id == OperatingDatesExceptions.vehicle_journey_id,
        )
        .outerjoin(
            NonOperatingdatesexceptions,
            VehicleJourney.id == NonOperatingdatesexceptions.vehicle_journey_id,
        )
        .outerjoin(
            ServicedOrganisationVehicleJourney,
            VehicleJourney.id == ServicedOrganisationVehicleJourney.vehicle_journey_id,
        )
        .where(Service.txcfileattributes_id == check.file_id)
        .with_entities(
            VehicleJourney.line_ref,
            VehicleJourney.journey_code,
            VehicleJourney.id.label("vehicle_journey_id"),
            VehicleJourney.direction,
            NonOperatingdatesexceptions.non_operating_date,
            OperatingDatesExceptions.operating_date,
            OperatingProfile.day_of_week,
            ServicePatternStop.id.label("service_pattern_stop_id"),
            ServicePatternStop.auto_sequence_number,
            ServicedOrganisationVehicleJourney.serviced_organisation_id,
        )
        .order_by(asc(VehicleJourney.id), asc(ServicePatternStop.auto_sequence_number))
    )

    df = pd.read_sql_query(result.statement, check.db.session.bind)

    return (
        df.groupby(["vehicle_journey_id", "line_ref", "journey_code"])
        .agg(
            {
                "non_operating_date": lambda x: [item.strftime("%Y-%m-%d") for item in x.unique() if item is not None],
                "operating_date": lambda x: [item.strftime("%Y-%m-%d") for item in x.unique() if item is not None],
                "day_of_week": lambda x: [item for item in x.unique() if item is not None],
                "service_pattern_stop_id": "first",
                "serviced_organisation_id": lambda x: [item for item in x.unique() if item is not None],
            }
        )
        .reset_index()
    )
