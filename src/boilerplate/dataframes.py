from common import Check
import pandas as pd
from sqlalchemy.sql.functions import coalesce


def get_df_vehicle_journey(check: Check) -> pd.DataFrame:
    """
    Get the dataframe containing the vehicle journey and the stop activity

    """

    Service = check.db.classes.transmodel_service
    ServicePatternService = check.db.classes.transmodel_service_service_patterns
    ServicePattern = check.db.classes.transmodel_servicepattern
    ServicePatternStop = check.db.classes.transmodel_servicepatternstop
    StopActivity = check.db.classes.transmodel_stopactivity
    VehicleJourney = check.db.classes.transmodel_vehiclejourney
    NaptanStopPoint = check.db.classes.naptan_stoppoint

    result = (
        check.db.session.query(Service)
        .join(ServicePatternService, Service.id == ServicePatternService.service_id)
        .join(
            ServicePattern, ServicePatternService.servicepattern_id == ServicePattern.id
        )
        .join(
            ServicePatternStop,
            ServicePattern.id == ServicePatternStop.service_pattern_id,
        )
        .join(StopActivity, ServicePatternStop.stop_activity_id == StopActivity.id)
        .join(
            VehicleJourney, ServicePatternStop.vehicle_journey_id == VehicleJourney.id
        )
        .join(NaptanStopPoint, ServicePatternStop.naptan_stop_id == NaptanStopPoint.id,isouter=True)
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
