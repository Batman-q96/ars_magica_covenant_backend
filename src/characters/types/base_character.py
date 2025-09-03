"""Generic character"""

from typing import Optional, Any

from dateutil import relativedelta
import pydantic

from characters.parts.wounds import (
    wound_tracker as parts_wounds,
)
from characters.types import i_character

from lib.time import time


def count_light_wound_periods_in_realtive_delta(
    duration: relativedelta.relativedelta,
) -> int:
    """Count the number of times we should make recovery rolls for light wounds"""
    return time.get_deltas_in_larger_relative_delta(
        short_duration=parts_wounds.LightWound.RECOVERY_PERIOD, long_duration=duration
    )


def count_medium_wound_periods_in_relative_delta(
    duration: relativedelta.relativedelta,
) -> int:
    """Count the number of times we should make recovery rolls for medium wounds"""
    return time.get_deltas_in_larger_relative_delta(
        short_duration=parts_wounds.MediumWound.RECOVERY_PERIOD, long_duration=duration
    )


def count_heavy_wound_periods_in_relative_delta(
    duration: relativedelta.relativedelta,
) -> int:
    """Count the number of times we should make recovery rolls for minor wounds"""
    return time.get_deltas_in_larger_relative_delta(
        short_duration=parts_wounds.LightWound.RECOVERY_PERIOD, long_duration=duration
    )


class BaseCharacter(i_character.ICharacter):
    """Base character class"""

    _wound_tracker: parts_wounds.WoundTracker = pydantic.PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        """Initialze base char as needed"""
        self._wound_tracker = parts_wounds.WoundTracker(size=self.size)

    def take_damage(self, damage: int) -> None:
        """Take a hit and add an appopriate wound"""
        self._wound_tracker.take_damage(damage)

    def recover(
        self,
        duration: relativedelta.relativedelta,
        recovery_bonus: int = 0,
        recovery_roll: Optional[int] = None,
    ) -> None:
        """Recover all wounds as appropriate based on the time duration"""
        wound_tracker = self._wound_tracker
        while wound_tracker.incapacitated:
            wound_tracker.recover_all_incapacitating_wounds(
                recovery_bonus=recovery_bonus, recovery_roll_results=recovery_roll
            )

    @property
    def incapacitated(self) -> bool:
        return self._wound_tracker.incapacitated

    @property
    def dead(self) -> bool:
        return self._wound_tracker.dead


b = BaseCharacter(
    traits=[],
    abilities=[],
    flaws=[],
    virtues=[],
    reputations=[],
)
print(b)
