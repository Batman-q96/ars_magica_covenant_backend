import enum


class WoundStatus(enum.Enum):
    """Enum to determine result of healing roll"""

    WORSE = -1
    SAME = 0
    BETTER = 1
