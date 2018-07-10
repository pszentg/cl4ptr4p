from enum import Enum


class SG90(Enum):
    MIN_DUTY = 3.0
    MAX_DUTY = 11.0
    # MIN_DUTY + (MAX_DUTY - MIN_DUTY) / 2 =
    CENTER = 7.0

