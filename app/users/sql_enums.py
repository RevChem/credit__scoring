from enum import IntEnum, Enum

class JobType(IntEnum):
    FULL_TIME = 0
    PART_TIME = 1
    SELF_EMPLOYED = 2
    RETIRED = 3


JOB_TYPE_MAP = {
    "Employed - full time": JobType.FULL_TIME,
    "Employed - part time": JobType.PART_TIME,
    "Self employed": JobType.SELF_EMPLOYED,
    "Retired": JobType.RETIRED
}


class Risk_Category(Enum):
    high = "high"
    low = "low"

