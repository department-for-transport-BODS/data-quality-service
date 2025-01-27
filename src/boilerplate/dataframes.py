from common import Check, DQSReport
import pandas as pd
import numpy as np
from sqlalchemy.sql.functions import coalesce
from typing import List
from sqlalchemy import and_, func, String, asc
from dqs_logger import logger
from data_persistence import PersistedData, PersistenceKey
from sqlalchemy import and_, func, String, asc, case


def get_df_vehicle_journey(check: Check, refresh=False) -> pd.DataFrame:
    """
    Get the dataframe containing the vehicle journey and the stop activity

    """

    persistence = PersistedData()
    if not refresh and persistence.exists(PersistenceKey.VEHICLE_JOURNEY.to_check_value(check)):
        logger.info(f"Returning persisted vehicle journey dataframe for {check.file_id}")
        return persistence.get(PersistenceKey.VEHICLE_JOURNEY.to_check_value(check))

    logger.info(f"Retrieving vehicle Journey DF for {check.file_id}")
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
            VehicleJourney.journey_code.label("vehicle_journey_code"),
        )
    )
    df = pd.read_sql_query(result.statement, check.db.session.bind)
    logger.info(f"Persisting Vehicle data DF for {check.file_id}")
    persistence.save(PersistenceKey.VEHICLE_JOURNEY.to_check_value(check), df)
    return df


def get_df_missing_bus_working_number(check: Check) -> pd.DataFrame:
    """
    Get the dataframe containing the vehicle journey for the missing bus block number

    """

    Service = check.db.classes.transmodel_service
    ServicePatternService = check.db.classes.transmodel_service_service_patterns
    VehicleJourney = check.db.classes.transmodel_vehiclejourney
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
            VehicleJourney,
            ServicePatternService.servicepattern_id
            == VehicleJourney.service_pattern_id,
        )
        .where(Service.txcfileattributes_id == check.file_id)
        .where(VehicleJourney.block_number == None)
        .group_by(
            VehicleJourney.id,
        )
        .with_entities(
            VehicleJourney.id.label("vehicle_journey_id"),
            VehicleJourney.start_time.label("start_time"),
            VehicleJourney.block_number.label("block_number"),
            VehicleJourney.direction.label("direction"),
            func.min(ServicePatternStop.id).label("service_pattern_stop_id"), # Get the first stop for Each Vehicle Journey
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

    df = pd.DataFrame.from_records(result, columns=columns)
    return df


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

    logger.info(f"Retrieving duplicate Journey Code DF {check.file_id}/{check.check_id}")
    Service = check.db.classes.transmodel_service
    ServicePatternService = check.db.classes.transmodel_service_service_patterns
    ServicePatternStop = check.db.classes.transmodel_servicepatternstop
    ServicedOrganisationVJ = check.db.classes.transmodel_servicedorganisationvehiclejourney

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
        .join(
            ServicedOrganisationVJ,
            ServicedOrganisationVJ.vehicle_journey_id == VehicleJourney.id,
            isouter=True,
            full=True,
        )
        .where(Service.txcfileattributes_id == check.file_id)
        .with_entities(
            VehicleJourney.line_ref,
            VehicleJourney.journey_code,
            VehicleJourney.id.label("vehicle_journey_id"),
            VehicleJourney.direction,
            ServicePatternStop.id.label("service_pattern_stop_id"),
            ServicePatternStop.auto_sequence_number,
            ServicedOrganisationVJ.operating_on_working_days.label(
                "operating_on_working_days"
            ),
        )
        .order_by(asc(VehicleJourney.id), asc(ServicePatternStop.auto_sequence_number))
    )

    df = pd.read_sql_query(result.statement, check.db.session.bind)
    df.fillna({"operating_on_working_days": np.nan}, inplace=True)
    vehicle_journey_df = (
        df.groupby(
            [
                "vehicle_journey_id",
                "line_ref",
                "journey_code",
                "operating_on_working_days",
            ],
            dropna=False,
        )
        .agg(
            {
                "service_pattern_stop_id": "first",
            }
        )
        .reset_index()
    )

    vehicle_journey_ids = list(vehicle_journey_df["vehicle_journey_id"])
    operating_profile_df = get_operating_profile_df(check, vehicle_journey_ids)
    oprating_date_exp_df = get_operating_date_exception_df(check, vehicle_journey_ids)
    non_op_date_exp_df = get_non_operating_date_exception_df(check, vehicle_journey_ids)

    serviced_org_df = get_service_ogranisation_vehicle_journey_df(
        check, vehicle_journey_ids
    )

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


def get_df_serviced_organisation(check: Check) -> pd.DataFrame:
    """
    Get the dataframe containing the serviced organisation

    """

    Service = check.db.classes.transmodel_service
    ServicePatternService = check.db.classes.transmodel_service_service_patterns
    VehicleJourney = check.db.classes.transmodel_vehiclejourney
    ServiceOrganisationVehicleJourney = (
        check.db.classes.transmodel_servicedorganisationvehiclejourney
    )
    ServiceOrganisationWorkingDays = (
        check.db.classes.transmodel_servicedorganisationworkingdays
    )
    ServicedOrganisation = check.db.classes.transmodel_servicedorganisations

    result = (
        check.db.session.query(Service)
        .join(ServicePatternService, Service.id == ServicePatternService.service_id)
        .join(
            VehicleJourney,
            ServicePatternService.servicepattern_id
            == VehicleJourney.service_pattern_id,
        )
        .join(
            ServiceOrganisationVehicleJourney,
            ServiceOrganisationVehicleJourney.vehicle_journey_id == VehicleJourney.id,
        )
        .join(
            ServicedOrganisation,
            ServiceOrganisationVehicleJourney.serviced_organisation_id
            == ServicedOrganisation.id,
        )
        .join(
            ServiceOrganisationWorkingDays,
            ServiceOrganisationWorkingDays.serviced_organisation_vehicle_journey_id
            == ServiceOrganisationVehicleJourney.id,
        )
        .where(
            and_(
                Service.txcfileattributes_id == check.file_id,
                ServiceOrganisationVehicleJourney.operating_on_working_days == True,
            )
        )
        .with_entities(
            VehicleJourney.id.label("vehicle_journey_id"),
            ServicedOrganisation.id.label("serviced_organisation_id"),
            ServicedOrganisation.name.label("serviced_organisation_name"),
            ServicedOrganisation.organisation_code.label("serviced_organisation_code"),
            ServiceOrganisationWorkingDays.start_date.label(
                "serviced_organisation_start_date"
            ),
            ServiceOrganisationWorkingDays.end_date.label(
                "serviced_organisation_end_date"
            ),
            ServiceOrganisationVehicleJourney.id.label(
                "serviced_organisation_vehicle_journey_id"
            ),
        )
    )

    return pd.read_sql_query(result.statement, check.db.session.bind)


def get_naptan_availablilty(check: Check, atco_codes: set[String]) -> pd.DataFrame:
    """
    Get the naptan atco code availability and returned the dataframe containing the extra
    column atco_code_exists returns the boolean value which is True if the atco code is available
    otherwise False
    """

    NaptanStopPoint = check.db.classes.naptan_stoppoint

    result = check.db.session.query(
        NaptanStopPoint,
        case(
            (func.lower(NaptanStopPoint.atco_code).in_(atco_codes), True), else_=False
        ).label(
            "atco_code_exists"
        ),  # Label the new column as "atco_code_exists"
    ).where(func.lower(NaptanStopPoint.atco_code).in_(atco_codes))

    return pd.read_sql_query(result.statement, check.db.session.bind)
