from common import Check
import pandas as pd
from sqlalchemy.sql.functions import coalesce
from typing import List
from sqlalchemy import and_

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
