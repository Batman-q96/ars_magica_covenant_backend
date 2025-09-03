"""A standard wound is a light, medium, heavy, or incapacitating wound"""

from typing import ClassVar
import datetime

from dateutil import relativedelta
import pydantic

from lib import am5_rolls
from characters.parts.wounds import wound_status, i_wound


class StandardWound(i_wound.IWound):
    """Standard wounds are light, medium, heavy, and incapacitating"""

    bonus: int
    _STABLE_EASE_FACTOR: ClassVar[int]
    _RECOVERY_EASE_FACTOR: ClassVar[int]
    _STABLE_RECOVERY_BONUS: ClassVar[int] = 3
    recovery_bonus: int = pydantic.Field(default=0, ge=0, multiple_of=3)
    RECOVERY_PERIOD: relativedelta.relativedelta
    _time_to_next_recovery_check: relativedelta.relativedelta = pydantic.Field()

    def heal_based_on_recovery_result(self, recovery_result: int) -> None:
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

    def make_recovery_roll(self) -> None:
        """Make a recovery roll for this wound"""
        try:
            self.heal_based_on_recovery_result(
                am5_rolls.roll_stress(modifier=self.recovery_bonus)
            )
        except am5_rolls.BotchedRollExcption:
            self.status = wound_status.WoundStatus.WORSE

    def heal_based_on_time_passed(
        self, time_passed: relativedelta.relativedelta
    ) -> relativedelta.relativedelta:
        """Heal the wound a numeber of times based on time passed"""
        while time_passed >= self._time_to_next_recovery_check:
            self.make_recovery_roll()
            time_passed -= self.RECOVERY_PERIOD
