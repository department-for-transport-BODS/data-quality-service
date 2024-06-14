from enum import Enum, unique

class DQSTaskResultStatus(str, Enum):

    PENDING = "PENDING"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"
    SUCCESS = "SUCCESS"
    DUMMY_SUCCESS = "DUMMY_SUCCESS"

class DQReportStatus(str, Enum):
    PIPELINE_PENDING = "PIPELINE_PENDING"
    PIPELINE_SUCCEEDED = "PIPELINE_SUCCEEDED"
    PIPELINE_SUCCEEDED_WITH_ERRORS = "PIPELINE_SUCCEEDED_WITH_ERRORS"
    PIPELINE_FAILED = "PIPELINE_FAILED"
    COMPLETED = "COMPLETED"
    COMPLETED_WITH_ERRORS = "COMPLETED_WITH_ERRORS"
    TIMEOUT = "TIMEOUT"

class Timeouts(int, Enum):
    TIMEOUT_HOURS = 12


@unique
class Level(Enum):
    critical = "Critical"
    advisory = "Advisory"


@unique
class Category(Enum):
    stops = "Stops"
    timing = "Timing"
    journey = "Journey"
    data_set = "Data set"


class CheckBasis(Enum):
    stops = "stops"
    lines = "lines"
    timing_patterns = "timing_patterns"
    vehicle_journeys = "vehicle_journeys"
    data_set = "data_set"
