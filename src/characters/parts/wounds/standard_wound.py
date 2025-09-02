"""A standard wound is a light, medium, heavy, or incapacitating wound"""

from typing import ClassVar
import datetime

from dateutil import relativedelta
import pydantic

from characters.parts.wounds import wound_status, i_wound


class StandardWound(i_wound.IWound):
    """Standard wounds are light, medium, heavy, and incapacitating"""

    bonus: int
    _STABLE_EASE_FACTOR: ClassVar[int]
    _RECOVERY_EASE_FACTOR: ClassVar[int]
    _STABLE_RECOVERY_BONUS: ClassVar[int] = 3
    recovery_bonus: int = pydantic.Field(default=0, ge=0, multiple_of=3)
    RECOVERY_PERIOD: relativedelta.relativedelta
    _last_recovery_check: datetime.datetime = pydantic.Field()

    def heal(self, recovery_result: int) -> None:
        """Healing for these wounds depends on their ease factors"""
        if recovery_result < self._STABLE_EASE_FACTOR:
            self.status = wound_status.WoundStatus.WORSE
        elif (
            self._STABLE_EASE_FACTOR <= recovery_result
            and recovery_result < self._RECOVERY_EASE_FACTOR
        ):
            self.status = wound_status.WoundStatus.SAME
            self.recovery_bonus += self._STABLE_RECOVERY_BONUS
        elif self._RECOVERY_EASE_FACTOR <= recovery_result:
            self.status = wound_status.WoundStatus.BETTER
        else:
            raise ValueError("Invalid recovery roll")
