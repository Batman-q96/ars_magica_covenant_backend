from typing import ClassVar

import pydantic


from lib.time import time

from characters.parts.wounds import standard_wound


class IncapacitatingWound(standard_wound.StandardWound):
    """Incapacitating wounds will prevent a character from enagaging in any serious activity"""

    bonus: ClassVar[None] = None
    _STABLE_EASE_FACTOR: ClassVar[int] = 0
    _RECOVERY_EASE_FACTOR: ClassVar[int] = 9
    _STABLE_RECOVERY_BONUS: ClassVar[int] = -1
    RECOVERY_PERIOD: ClassVar[time.RelativeDelta] = time.RelativeDelta(hours=12)
    recovery_bonus: int = pydantic.Field(default=0, le=0)
