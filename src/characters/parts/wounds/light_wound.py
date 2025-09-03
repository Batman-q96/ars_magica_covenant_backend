from typing import ClassVar


from lib.time import time

from characters.parts.wounds import standard_wound


class LightWound(standard_wound.StandardWound):
    """Light wounds are easiest to heal"""

    bonus: ClassVar[int] = -1
    _STABLE_EASE_FACTOR: ClassVar[int] = 4
    _RECOVERY_EASE_FACTOR: ClassVar[int] = 10
    _STABLE_RECOVERY_BONUS: ClassVar[int] = 3
    RECOVERY_PERIOD: ClassVar[time.RelativeDelta] = time.RelativeDelta(weeks=1)
