from common import Check, DQSReport
import pandas as pd
import geoalchemy2
from sqlalchemy.sql.functions import coalesce
from typing import List
from sqlalchemy import and_, func, String, asc
from dqs_logger import logger


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
            dqs_observationresults.details.label("Details"),
        )
        .join(
            dqs_taskresults, dqs_observationresults.taskresults_id == dqs_taskresults.id
        )
        .join(dqs_report, dqs_taskresults.dataquality_report_id == dqs_report.id)
        .join(dqs_checks, dqs_taskresults.checks_id == dqs_checks.id)
        .join(
            organisation_txcfileattributes,
            organisation_txcfileattributes.id
            == dqs_taskresults.transmodel_txcfileattributes_id,
        )
        .join(
            transmodel_service,
            transmodel_service.txcfileattributes_id
            == organisation_txcfileattributes.id,
        )
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

    Service = check.db.classes.transmodel_service
    ServicePatternService = check.db.classes.transmodel_service_service_patterns
    ServicePatternStop = check.db.classes.transmodel_servicepatternstop
    logger.info("Getting vehicle Journeys list....")
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
        .where(Service.txcfileattributes_id == check.file_id)
        .with_entities(
            VehicleJourney.line_ref,
            VehicleJourney.journey_code,
            VehicleJourney.id.label("vehicle_journey_id"),
            VehicleJourney.direction,
            ServicePatternStop.id.label("service_pattern_stop_id"),
            ServicePatternStop.auto_sequence_number,
        )
        .order_by(asc(VehicleJourney.id), asc(ServicePatternStop.auto_sequence_number))
    )

    df = pd.read_sql_query(result.statement, check.db.session.bind)

    vehicle_journey_df = (
        df.groupby(["vehicle_journey_id", "line_ref", "journey_code"])
        .agg(
            {
                "service_pattern_stop_id": "first",
            }
        )
        .reset_index()
    )

    logger.info("Fetched vehicle Journeys list")

    vehicle_journey_ids = list(vehicle_journey_df["vehicle_journey_id"])
    logger.info("Fetching Operating profile df...")
    operating_profile_df = get_operating_profile_df(check, vehicle_journey_ids)
    logger.info("Fetched Operating profile df")

    logger.info("Fetching Operating date exception df...")
    oprating_date_exp_df = get_operating_date_exception_df(check, vehicle_journey_ids)
    logger.info("Fetched Operating date exception df")

    logger.info("Fetching Non operating date exception df...")
    non_op_date_exp_df = get_non_operating_date_exception_df(check, vehicle_journey_ids)
    logger.info("Fetched Non operating date exception df")

    logger.info("Fetching Serviced organisation VJ df...")
    serviced_org_df = get_service_ogranisation_vehicle_journey_df(
        check, vehicle_journey_ids
    )
    logger.info("Fetched Serviced organisations VJ df")

    vehicle_journey_df = (
        vehicle_journey_df.merge(
            operating_profile_df,
            on="vehicle_journey_id",
            how="left",
        )
        .merge(
            oprating_date_exp_df,
            on="vehicle_journey_id",
            how="left",
        )
        .merge(
            non_op_date_exp_df,
            on="vehicle_journey_id",
            how="left",
        )
        .merge(
            serviced_org_df,
            on="vehicle_journey_id",
            how="left",
        )
    )

    vehicle_journey_df = vehicle_journey_df.fillna("[]")
    return vehicle_journey_df


def get_operating_profile_df(check: Check, vehicle_journey_ids: List) -> pd.DataFrame:
    """Get dataframe with the list of operating profile days for
    the list of vehicle journeys

    Args:
        check (Check): check object
        vehicle_journey_ids (List): list of vehicle journey ids

    Returns:
        pd.DataFrame: Dataframe with days_of_week list for vehicle journeys
    """
    OperatingProfile = check.db.classes.transmodel_operatingprofile
    result_op = (
        check.db.session.query(OperatingProfile)
        .with_entities(
            func.array_agg(func.distinct(OperatingProfile.day_of_week)).label(
                "day_of_week"
            ),
            OperatingProfile.vehicle_journey_id.label("vehicle_journey_id"),
        )
        .filter(OperatingProfile.vehicle_journey_id.in_(vehicle_journey_ids))
        .group_by(OperatingProfile.vehicle_journey_id)
    )
    return pd.read_sql_query(result_op.statement, check.db.session.bind)


def get_operating_date_exception_df(
    check: Check, vehicle_journey_ids: List
) -> pd.DataFrame:
    """Get dataframe with the list of operating_date_exceptions for
    the list of vehicle journeys

    Args:
        check (Check): Check object
        vehicle_journey_ids (List): list of vehicle journey ids

    Returns:
        pd.DataFrame: Dataframe with Operating_date_exceptions
    """
    OperatingDatesExceptions = check.db.classes.transmodel_operatingdatesexceptions
    result_op_date_exp = (
        check.db.session.query(OperatingDatesExceptions)
        .with_entities(
            func.array_agg(
                func.distinct(
                    func.to_char(OperatingDatesExceptions.operating_date, "YYYY-MM-DD")
                )
            ).label("operating_date"),
            OperatingDatesExceptions.vehicle_journey_id.label("vehicle_journey_id"),
        )
        .filter(OperatingDatesExceptions.vehicle_journey_id.in_(vehicle_journey_ids))
        .group_by(OperatingDatesExceptions.vehicle_journey_id)
    )

    return pd.read_sql_query(result_op_date_exp.statement, check.db.session.bind)


def get_non_operating_date_exception_df(
    check: Check, vehicle_journey_ids: List
) -> pd.DataFrame:
    """Get dataframe with the list of non_operating_date_exceptions for
    the list of vehicle journeys

    Args:
        check (Check): Check object
        vehicle_journey_ids (List): list of vehicle journies

    Returns:
        pd.DataFrame: dataframe with non_operating_date_exceptions
    """
    NonOperatingdatesexceptions = (
        check.db.classes.transmodel_nonoperatingdatesexceptions
    )
    result_non_op_date_exp = (
        check.db.session.query(NonOperatingdatesexceptions)
        .with_entities(
            func.array_agg(
                func.distinct(
                    func.to_char(
                        NonOperatingdatesexceptions.non_operating_date, "YYYY-MM-DD"
                    )
                )
            ).label("non_operating_date"),
            NonOperatingdatesexceptions.vehicle_journey_id.label("vehicle_journey_id"),
        )
        .filter(NonOperatingdatesexceptions.vehicle_journey_id.in_(vehicle_journey_ids))
        .group_by(NonOperatingdatesexceptions.vehicle_journey_id)
    )

    return pd.read_sql_query(result_non_op_date_exp.statement, check.db.session.bind)


def get_service_ogranisation_vehicle_journey_df(
    check: Check, vehicle_journey_ids: List
) -> pd.DataFrame:
    """Get dataframe for serviced organisations belonging to
    Vehicle journeys

    Args:
        check (Check):
        vehicle_journey_ids (List): List of vehicle journeys list

    Returns:
        pd.DataFrame: Dataframe with serviced organisations
    """
    ServicedOrganisationVehicleJourney = (
        check.db.classes.transmodel_servicedorganisationvehiclejourney
    )
    result_serviced_organisation = (
        check.db.session.query(ServicedOrganisationVehicleJourney)
        .with_entities(
            func.array_agg(
                func.distinct(
                    func.cast(
                        ServicedOrganisationVehicleJourney.serviced_organisation_id,
                        String,
                    )
                )
            ).label("serviced_organisation_id"),
            ServicedOrganisationVehicleJourney.vehicle_journey_id.label(
                "vehicle_journey_id"
            ),
        )
        .filter(
            ServicedOrganisationVehicleJourney.vehicle_journey_id.in_(
                vehicle_journey_ids
            )
        )
        .group_by(ServicedOrganisationVehicleJourney.vehicle_journey_id)
    )

    return pd.read_sql_query(
        result_serviced_organisation.statement, check.db.session.bind
    )
