from common import Check, DQSReport
import pandas as pd
import geoalchemy2
from sqlalchemy.sql.functions import coalesce
from typing import List
from sqlalchemy import and_, select


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
            ServicePatternStop.sequence_number.label("sequence_number"),
            ServicePatternStop.atco_code.label("atco_code"),
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
    print("In the DQS REPORT QUERY::")
    dqs_observationresults = report.db.classes.dqs_observationresults
    dqs_taskresults = report.db.classes.dqs_taskresults
    dqs_report = report.db.classes.dqs_report
    dqs_checks = report.db.classes.dqs_checks
    organisation_txcfileattributes = report.db.classes.organisation_txcfileattributes
    transmodel_service = report.db.classes.transmodel_service

    query = (
        select([
            dqs_checks.importance,
            dqs_checks.category,
            dqs_checks.observation,
            transmodel_service.service_code,
            transmodel_service.name.label("line_name"),
            dqs_observationresults.details,
            # organisation_txcfileattributes.details,
            # dqs_observationresults.vehicle_journey_id
        ])
        .select_from(
            dqs_observationresults
            .join(dqs_taskresults, dqs_observationresults.c.taskresults_id == dqs_taskresults.id)
            .join(dqs_report, dqs_taskresults.c.dataquality_report_id == dqs_report.id)
            .join(dqs_checks, dqs_taskresults.c.checks_id == dqs_checks.id)
            .join(organisation_txcfileattributes, organisation_txcfileattributes.c.id == dqs_taskresults.c.transmodel_txcfileattributes_id)
            .join(transmodel_service, transmodel_service.c.txcfileattributes_id == organisation_txcfileattributes.c.id)
        )
        .where(dqs_report.id == report.report_id)
    )

    results = report.db.session.execute(query).fetchall()

    columns = [
        "importance",
        "category",
        "type_of_observation"
        "service_code",
        "line_name",
        "data_quality_observation",
    ]
    
    df = pd.DataFrame.from_records(results, columns=columns)
    print(f"The dataframe is :: {df}")
    return df

