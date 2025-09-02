from typing import ClassVar
from dateutil import relativedelta

from characters.parts.wounds import standard_wound


class HeavyWound(standard_wound.StandardWound):
    """Heavy wounds are the most serious typical wounds"""

    bonus: ClassVar[int] = -5
    _STABLE_EASE_FACTOR: ClassVar[int] = 9
    _RECOVERY_EASE_FACTOR: ClassVar[int] = 15
    _STABLE_RECOVERY_BONUS: ClassVar[int] = 3
    RECOVERY_PERIOD: ClassVar[relativedelta.relativedelta] = (
        relativedelta.relativedelta(months=3)
    )
