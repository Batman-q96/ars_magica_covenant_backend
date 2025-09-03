from typing import ClassVar


from lib.time import time

from characters.parts.wounds import standard_wound


class MediumWound(standard_wound._StandardWound):
    """Medium wounds are more serious than light ones"""

    bonus: ClassVar[int] = -3
    _STABLE_EASE_FACTOR: ClassVar[int] = 6
    _RECOVERY_EASE_FACTOR: ClassVar[int] = 12
    _STABLE_RECOVERY_BONUS: ClassVar[int] = 3
    RECOVERY_PERIOD: ClassVar[time.RelativeDelta] = time.RelativeDelta(months=1)
