from enum import IntEnum, Enum

class JobType(IntEnum):
    FULL_TIME = 0
    PART_TIME = 1
    SELF_EMPLOYED = 2
    RETIRED = 3


class Risk_Category(Enum):
    high = "high"
    low = "low"
