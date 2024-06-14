from enum import Enum


class DQSTaskResultStatus(str, Enum):

    PENDING = "PENDING"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"
    DUMMY_SUCCESS = "DUMMY_SUCCESS"
